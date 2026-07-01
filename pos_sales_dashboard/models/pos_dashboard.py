from odoo import models, api
from datetime import datetime, timedelta
from calendar import monthrange


class PosDashboard(models.Model):
    _name = "pos.sales.dashboard"
    _description = "POS Dashboard"

    @api.model
    def get_dashboard_data(
        self,
        filter_type="today",
        session_id=False,
        product_id=False,
        store_id=False,
        category_id=False,
        cashier_id=False,
        payment_method_id=False):

        today = datetime.today()
        company_id = self.env.company.id

        # -----------------------------
        # DATE FILTER
        # -----------------------------
        if filter_type == "today":
            date_from = today.date()
        elif filter_type == "week":
            date_from = (today - timedelta(days=7)).date()
        elif filter_type == "month":
            date_from = today.replace(day=1).date()
        elif filter_type == "year":
            date_from = today.replace(month=1, day=1).date()
        elif filter_type == "yesterday":
            date_from = (today - timedelta(days=1)).date()
        else:
            date_from = today.date()

        # -----------------------------
        # ORDER DOMAIN (DATE + SESSION)
        # -----------------------------
        if filter_type in ['today', 'yesterday']:

            date_start = datetime.combine(
                date_from,
                datetime.min.time()
            )

            date_end = datetime.combine(
                date_from,
                datetime.max.time()
            )

            domain = [
                ('date_order', '>=', date_start),
                ('date_order', '<=', date_end),
                ('company_id', '=', company_id)
            ]

        else:
            domain = [
                ('date_order', '>=', date_from),
                ('company_id', '=', company_id)
            ]

        if session_id:
            domain.append(('session_id', '=', session_id))


        # Sidebar Filters
        if store_id:
            domain.append(('config_id', '=', int(store_id)))

        if cashier_id:
            domain.append(('employee_id', '=', int(cashier_id)))

        if product_id:
            domain.append(('lines.product_id', '=', int(product_id)))

        orders = self.env['pos.order'].search(domain)

        total_sales = sum(orders.mapped("amount_total"))
        total_order_count = len(orders)

        lang = self.env.lang or 'en_US'

        # ---------------------------------------------------------
        # TOP PRODUCTS
        # ---------------------------------------------------------
        if filter_type in ['today', 'yesterday']:
            product_query = """
                SELECT pol.product_id,
                       SUM(pol.qty),
                       SUM(pol.qty * pol.price_unit)
                FROM pos_order_line pol
                JOIN pos_order po ON pol.order_id = po.id
                WHERE DATE(po.date_order) = %s
                AND po.company_id = %s
            """
        else:
            product_query = """
                SELECT pol.product_id,
                       SUM(pol.qty),
                       SUM(pol.qty * pol.price_unit)
                FROM pos_order_line pol
                JOIN pos_order po ON pol.order_id = po.id
                WHERE DATE(po.date_order) >= %s
                AND po.company_id = %s
            """

        params = [date_from, company_id]

        if session_id:
            product_query += " AND po.session_id = %s"
            params.append(session_id)

        product_query += """
            GROUP BY pol.product_id
            ORDER BY SUM(pol.qty) DESC
            LIMIT 30
        """

        self.env.cr.execute(product_query, tuple(params))
        product_rows = self.env.cr.fetchall()

        product_ids = [r[0] for r in product_rows]

        products = []

        if product_ids:
            product_records = self.env['product.product'].browse(product_ids)

            qty_map = {r[0]: r[1] for r in product_rows}
            amount_map = {r[0]: r[2] for r in product_rows}

            for product in product_records:
                products.append(
                    (
                        product.display_name,
                        qty_map.get(product.id, 0),
                        product.id,
                        amount_map.get(product.id, 0)
                    )
                )

        # ---------------------------------------------------------
        # STORE PERFORMANCE
        # ---------------------------------------------------------
        if filter_type in ['today', 'yesterday']:
            store_query = """
                SELECT pc.name,
                       COUNT(po.id),
                       SUM(po.amount_total)
                FROM pos_order po
                JOIN pos_config pc ON po.config_id = pc.id
                WHERE DATE(po.date_order) = %s
                AND po.company_id = %s
            """
        else:
            store_query = """
                SELECT pc.name,
                       COUNT(po.id),
                       SUM(po.amount_total)
                FROM pos_order po
                JOIN pos_config pc ON po.config_id = pc.id
                WHERE DATE(po.date_order) >= %s
                AND po.company_id = %s
            """

        params = [date_from, company_id]

        if session_id:
            store_query += " AND po.session_id = %s"
            params.append(session_id)

        store_query += """
            GROUP BY pc.name
            ORDER BY SUM(po.amount_total) DESC
        """

        self.env.cr.execute(store_query, tuple(params))
        stores = self.env.cr.fetchall()

        # STORE RANKING
        store_ranking = []
        rank = 1

        for store in stores:
            store_ranking.append({
                "rank": rank,
                "store": store[0],
                "orders": store[1],
                "sales": store[2] or 0,
            })
            rank += 1

        # ---------------------------------------------------------
        # PAYMENT METHODS
        # ---------------------------------------------------------
        if filter_type in ['today', 'yesterday']:
            payment_query = f"""
                SELECT ppm.name->>'{lang}' AS name,
                       SUM(pp.amount) AS total
                FROM pos_payment pp
                JOIN pos_payment_method ppm ON pp.payment_method_id = ppm.id
                JOIN pos_order po ON pp.pos_order_id = po.id
                WHERE DATE(po.date_order) = %s
                AND po.company_id = %s
            """
        else:
            payment_query = f"""
                SELECT ppm.name->>'{lang}' AS name,
                       SUM(pp.amount) AS total
                FROM pos_payment pp
                JOIN pos_payment_method ppm ON pp.payment_method_id = ppm.id
                JOIN pos_order po ON pp.pos_order_id = po.id
                WHERE DATE(po.date_order) >= %s
                AND po.company_id = %s
            """

        params = [date_from, company_id]

        if session_id:
            payment_query += " AND po.session_id = %s"
            params.append(session_id)

        payment_query += f"""
            GROUP BY ppm.name->>'{lang}'
            ORDER BY total DESC
        """

        self.env.cr.execute(payment_query, tuple(params))
        payments = self.env.cr.fetchall()

        # ---------------------------------------------------------
        # TOP CUSTOMERS
        # ---------------------------------------------------------
        if filter_type in ['today', 'yesterday']:
            customer_query = """
                SELECT rp.id,
                       rp.name,
                       SUM(po.amount_total) AS total
                FROM pos_order po
                JOIN res_partner rp ON po.partner_id = rp.id
                WHERE po.partner_id IS NOT NULL
                AND DATE(po.date_order) = %s
                AND po.company_id = %s
            """
        else:
            customer_query = """
                SELECT rp.id,
                       rp.name,
                       SUM(po.amount_total) AS total
                FROM pos_order po
                JOIN res_partner rp ON po.partner_id = rp.id
                WHERE po.partner_id IS NOT NULL
                AND DATE(po.date_order) >= %s
                AND po.company_id = %s
            """

        params = [date_from, company_id]

        if session_id:
            session = self.env['pos.session'].browse(session_id)
            customer_query += " AND po.config_id = %s"
            params.append(session.config_id.id)

        customer_query += """
            GROUP BY rp.id, rp.name
            ORDER BY total DESC
            LIMIT 10
        """

        self.env.cr.execute(customer_query, tuple(params))
        customers = self.env.cr.fetchall()

        # ---------------------------------------------------------
        # USER INFO
        # ---------------------------------------------------------

        user = self.env.user

        user_data = {
            "name": user.name,
            "image": f"/web/image/res.users/{user.id}/image_128"
        }


        # ---------------------------------------------------------
        # POS SESSION STATUS COUNTS
        # ---------------------------------------------------------

        open_session_domain = [
            ('state', '=', 'opened'),
            ('company_id', '=', company_id)
        ]

        closed_session_domain = [
            ('state', '=', 'closed'),
            ('company_id', '=', company_id)
        ]

        if session_id:
            open_session_domain.append(('id', '=', session_id))
            closed_session_domain.append(('id', '=', session_id))

        open_sessions = self.env['pos.session'].search_count(open_session_domain)
        closed_sessions = self.env['pos.session'].search_count(closed_session_domain)

        # ---------------------------------------------------------
        # ACTIVE POS SESSIONS
        # ---------------------------------------------------------

        session_domain = [
            ('state', '=', 'opened'),
            ('company_id', '=', company_id)
        ]

        if session_id:
            session_domain.append(('id', '=', session_id))

        sessions = self.env['pos.session'].search(session_domain)

        session_data = [{
            "id": s.id,
            "name": s.config_id.name,
            "session": s.name,
            "user": s.user_id.name,
            "config": s.config_id.name,
            "start_at":s.start_at,
        } for s in sessions]


        # currency

        currency = self.env.company.currency_id

        currency_data = {
            "symbol": currency.symbol,
            "position": currency.position,  # before / after
        }

        # ---------------------------------------------------------
        # ALL SESSIONS
        # ---------------------------------------------------------

        all_sessions = self.env['pos.session'].search([
            ('state', '=', 'opened'),
            ('company_id', '=', company_id)
        ])

        all_session_data = [{
            "id": s.id,
            "name": s.config_id.name,
            "session": s.name,
            "user": s.user_id.name,
            "config": s.config_id.name
        } for s in all_sessions]


        # ---------------------------------------------------------
        # ---------------------------------------------------------
        # TOP POS CATEGORIES
        # ---------------------------------------------------------
        # Get relation metadata from field definition
        field = self.env['product.template']._fields['pos_categ_ids']
        relation_table = field.relation
        col1 = field.column1
        col2 = field.column2
        if filter_type in ['today', 'yesterday']:
            category_query = f"""
                SELECT pc.id,
                       pc.name,
                       SUM(pol.qty) AS qty_sold
                FROM pos_order_line pol
                JOIN pos_order po ON pol.order_id = po.id
                JOIN product_product pp ON pol.product_id = pp.id
                JOIN product_template pt ON pp.product_tmpl_id = pt.id
                JOIN {relation_table} rel ON rel.{col1} = pt.id
                JOIN pos_category pc ON pc.id = rel.{col2}
                WHERE DATE(po.date_order) = %s
                AND po.company_id = %s
            """
        else:
            category_query = f"""
                SELECT pc.id,
                       pc.name,
                       SUM(pol.qty) AS qty_sold
                FROM pos_order_line pol
                JOIN pos_order po ON pol.order_id = po.id
                JOIN product_product pp ON pol.product_id = pp.id
                JOIN product_template pt ON pp.product_tmpl_id = pt.id
                JOIN {relation_table} rel ON rel.{col1} = pt.id
                JOIN pos_category pc ON pc.id = rel.{col2}
                WHERE DATE(po.date_order) >= %s
                AND po.company_id = %s
            """

        params = [date_from, company_id]

        if session_id:
            category_query += " AND po.session_id = %s"
            params.append(session_id)

        category_query += """
            GROUP BY pc.id, pc.name
            ORDER BY SUM(pol.qty) DESC
            LIMIT 10
        """

        self.env.cr.execute(category_query, tuple(params))
        rows = self.env.cr.fetchall()

        categories = []

        for r in rows:
            name = r[1]

            if isinstance(name, dict):
                name = name.get(self.env.lang, list(name.values())[0])

            categories.append({
                "id": r[0],
                "name": name,
                "qty": r[2],
            })



        # ---------------------------------------------------------
        # TOP CASHIERS (Employee)
        # ---------------------------------------------------------

        top_cashiers = []

        if filter_type in ['today', 'yesterday']:
            cashier_query = """
                SELECT 
                    he.id,
                    he.name,
                    COUNT(po.id) AS orders,
                    COALESCE(SUM(po.amount_total), 0) AS sales
                FROM pos_order po
                JOIN hr_employee he ON po.employee_id = he.id
                WHERE DATE(po.date_order) = %s
                AND po.company_id = %s
            """
        else:
            cashier_query = """
                SELECT 
                    he.id,
                    he.name,
                    COUNT(po.id) AS orders,
                    COALESCE(SUM(po.amount_total), 0) AS sales
                FROM pos_order po
                JOIN hr_employee he ON po.employee_id = he.id
                WHERE DATE(po.date_order) >= %s
                AND po.company_id = %s
            """

        params = [date_from, company_id]

        # Optional session filter
        if session_id:
            cashier_query += " AND po.session_id = %s"
            params.append(session_id)

        cashier_query += """
            GROUP BY he.id, he.name
            ORDER BY sales DESC
            LIMIT 10
        """

        self.env.cr.execute(cashier_query, tuple(params))
        cashier_rows = self.env.cr.fetchall()
        rank = 1
        for row in cashier_rows:
            top_cashiers.append({
                "rank": rank,
                "id": row[0],
                "name": row[1],
                "orders": row[2],
                "sales": float(row[3] or 0),
            })
            rank += 1

        # ---------------------------------------------------------
        # STORE SALES COMPARISON (BASED ON FILTER)
        # ---------------------------------------------------------
        if filter_type == "month":
            # -------------------------
            # CURRENT MONTH
            # -------------------------
            current_start = today.replace(day=1).date()

            # full month end
            last_day = monthrange(today.year, today.month)[1]
            current_end = today.replace(day=last_day).date()

            # -------------------------
            # PREVIOUS MONTH
            # -------------------------
            prev_month_date = current_start - timedelta(days=1)

            previous_start = prev_month_date.replace(day=1)

            prev_last_day = monthrange(prev_month_date.year, prev_month_date.month)[1]
            previous_end = prev_month_date.replace(day=prev_last_day)

        elif filter_type == "year":

            current_start = today.replace(month=1, day=1).date()
            current_end = today.date()

            previous_start = current_start.replace(year=current_start.year - 1)
            previous_end = current_start

        else:
            period_days = (today.date() - date_from).days + 1

            current_start = date_from
            current_end = today.date()

            previous_start = current_start - timedelta(days=period_days)
            previous_end = current_start


        # ---------------------------------------------------------
        # DATETIME CONVERSION
        # ---------------------------------------------------------

        current_start_dt = datetime.combine(current_start, datetime.min.time())
        current_end_dt = datetime.combine(current_end, datetime.max.time())
        previous_start_dt = datetime.combine(previous_start, datetime.min.time())
        previous_end_dt = datetime.combine(previous_end, datetime.max.time())
        if session_id:
            session = self.env['pos.session'].browse(session_id)
            config_id = session.config_id.id

            current_session_filter = "AND po.config_id = %s"
            previous_session_filter = "AND po.config_id = %s"
        else:
            current_session_filter = ""
            previous_session_filter = ""
            config_id = False


        comparison_query = """
            SELECT pc.name,

                SUM(CASE 
                    WHEN po.date_order >= %s 
                    AND po.date_order <= %s
                    {current_session_filter}
                    THEN po.amount_total ELSE 0
                END) AS current_sales,

                SUM(CASE 
                    WHEN po.date_order >= %s 
                    AND po.date_order <= %s
                    {previous_session_filter}
                    THEN po.amount_total ELSE 0
                END) AS previous_sales

            FROM pos_order po
            JOIN pos_config pc ON po.config_id = pc.id
            WHERE po.company_id = %s
        """

        comparison_query = comparison_query.format(
            current_session_filter=current_session_filter,
            previous_session_filter=previous_session_filter
        )

        # ---------------------------------------------------------
        # PARAMS (UPDATED)
        # ---------------------------------------------------------

        params = [
            current_start_dt,
            current_end_dt,
        ]

        if session_id:
            params.append(config_id)

        params += [
            previous_start_dt,
            previous_end_dt,
        ]

        if session_id:
            params.append(config_id)

        params.append(company_id)
        comparison_query += """
            GROUP BY pc.name
            ORDER BY pc.name
        """

        self.env.cr.execute(comparison_query, tuple(params))
        rows = self.env.cr.fetchall()
        store_comparison = []
        for r in rows:
            store_comparison.append({
                "store": r[0],
                "current": r[1] or 0,
                "previous": r[2] or 0,
            })
        # ---------------------------------------------------------
        # NOTIFICATIONS
        # ---------------------------------------------------------

        today_date = datetime.today().date()

        param_key = f"pos_dashboard_last_seen_{user.id}"

        last_seen_id = int(
            self.env['ir.config_parameter'].sudo().get_param(param_key, 0)
        )

        notification_query = """
            SELECT id, name, amount_total
            FROM pos_order
            WHERE DATE(date_order) = %s
            AND id > %s
            AND company_id = %s
        """

        params = [today_date, last_seen_id, company_id]

        if session_id:
            notification_query += " AND session_id = %s"
            params.append(session_id)

        notification_query += """
            ORDER BY id DESC
            LIMIT 10
        """

        self.env.cr.execute(notification_query, tuple(params))
        notification_orders = self.env.cr.fetchall()
        notification_count = len(notification_orders)
        return {
            "total_sales": round(total_sales, 2),
            "products": products,
            "stores": stores,
            "store_ranking": store_ranking,
            "payments": payments,
            "customers": customers,
            "total_order_count": total_order_count,
            "sessions": session_data,
            "all_sessions": all_session_data,
            "user": user_data,
            "notifications": notification_orders,
            "categories": categories,
            "notification_count": notification_count,
            "currency": currency_data,
            "open_sessions": open_sessions,
            "closed_sessions": closed_sessions,
            "store_comparison": store_comparison,
            "top_cashiers": top_cashiers,
            # Sidebar Filters
    'all_products': [
        {'id': p.id, 'name': p.display_name}
        for p in self.env['product.product'].search([])
    ],

    'all_stores': [
        {'id': s.id, 'name': s.name}
        for s in self.env['pos.config'].search([])
    ],

    'all_categories': [
        {'id': c.id, 'name': c.name}
        for c in self.env['pos.category'].search([])
    ],

    'all_cashiers': [
        {'id': e.id, 'name': e.name}
        for e in self.env['hr.employee'].search([])
    ],

    'all_payment_methods': [
        {'id': p.id, 'name': p.name}
        for p in self.env['pos.payment.method'].search([])
    ],
        }

    # notification for new orders
    @api.model
    def get_latest_order_id(self):
        order = self.env['pos.order'].search(
            [],
            order='id desc',
            limit=1
        )
        return order.id or 0

    # Product Details
    @api.model
    def get_product_sales_details(self, product_id, filter_type="today", session_id=False):

        today = datetime.today()
        company_id = self.env.company.id

        if filter_type == "today":
            date_from = today.date()
        elif filter_type == "week":
            date_from = (today - timedelta(days=7)).date()
        elif filter_type == "month":
            date_from = today.replace(day=1).date()
        elif filter_type == "year":
            date_from = today.replace(month=1, day=1).date()
        elif filter_type == "yesterday":
            date_from = (today - timedelta(days=1)).date()
        else:
            date_from = today.date()

        query = """
            SELECT pol.id,
                   po.name,
                   po.date_order,
                   pol.qty,
                   pol.price_unit,
                   pol.qty * pol.price_unit
            FROM pos_order_line pol
            JOIN pos_order po ON pol.order_id = po.id
            WHERE pol.product_id = %s
            AND DATE(po.date_order) >= %s
            AND po.company_id = %s
        """

        params = [product_id, date_from, company_id]

        if session_id:
            query += " AND po.session_id = %s"
            params.append(session_id)

        query += """
            ORDER BY po.date_order DESC
            LIMIT 30
        """

        self.env.cr.execute(query, tuple(params))
        rows = self.env.cr.fetchall()

        result = []

        for r in rows:
            result.append({
                "id": r[0],
                "order": r[1],
                "date": r[2],
                "qty": r[3],
                "price": r[4],
                "total": r[5],
            })

        return result


    @api.model
    def mark_notifications_read(self):

        user = self.env.user

        last_order = self.env['pos.order'].search(
            [('company_id', '=', self.env.company.id)],
            order="id desc",
            limit=1
        )

        param_key = f"pos_dashboard_last_seen_{user.id}"

        self.env['ir.config_parameter'].sudo().set_param(
            param_key,
            last_order.id if last_order else 0
        )

        return True

    # category related product
    @api.model
    def get_category_products(self, category_id, filter_type="today", session_id=False):

        from datetime import datetime, timedelta

        today = datetime.today()
        company_id = self.env.company.id

        if filter_type == "today":
            date_from = today.date()
        elif filter_type == "week":
            date_from = (today - timedelta(days=7)).date()
        elif filter_type == "month":
            date_from = today.replace(day=1).date()
        elif filter_type == "year":
            date_from = today.replace(month=1, day=1).date()
        elif filter_type == "yesterday":
            date_from = (today - timedelta(days=1)).date()
        else:
            date_from = today.date()

        domain = [
            ('order_id.date_order', '>=', date_from),
            ('order_id.company_id', '=', company_id),
            ('product_id.product_tmpl_id.pos_categ_ids', 'in', [category_id]),
        ]

        if session_id:
            domain.append(('order_id.session_id', '=', session_id))

        lines = self.env['pos.order.line'].search(domain)

        products = {}

        for line in lines:
            product = line.product_id
            qty = line.qty

            if product.id not in products:
                products[product.id] = {
                    "id": product.id,
                    "name": product.display_name,
                    "qty": 0
                }

            products[product.id]["qty"] += qty

        result = sorted(
            products.values(),
            key=lambda x: x["qty"],
            reverse=True
        )[:30]

        return result


    # Payment Method details
    @api.model
    def get_payment_method_details(
            self,
            payment_method,
            filter_type="today",
            session_id=False):

        today = datetime.today()
        company_id = self.env.company.id

        if filter_type == "today":
            date_from = today.date()
        elif filter_type == "week":
            date_from = (today - timedelta(days=7)).date()
        elif filter_type == "month":
            date_from = today.replace(day=1).date()
        elif filter_type == "year":
            date_from = today.replace(month=1, day=1).date()
        elif filter_type == "yesterday":
            date_from = (today - timedelta(days=1)).date()
        else:
            date_from = today.date()

        lang = self.env.lang or 'en_US'

        query = f"""
            SELECT
                pc.name,
                COUNT(po.id),
                SUM(pp.amount)
            FROM pos_payment pp
            JOIN pos_payment_method ppm
                ON pp.payment_method_id = ppm.id
            JOIN pos_order po
                ON pp.pos_order_id = po.id
            JOIN pos_config pc
                ON po.config_id = pc.id
            WHERE ppm.name->>'{lang}' = %s
            AND po.company_id = %s
            AND DATE(po.date_order) >= %s
        """

        params = [payment_method, company_id, date_from]

        if session_id:
            query += " AND po.session_id = %s"
            params.append(session_id)

        query += """
            GROUP BY pc.name
            ORDER BY SUM(pp.amount) DESC
        """

        self.env.cr.execute(query, tuple(params))

        return [
            {
                "store": r[0],
                "orders": r[1],
                "amount": r[2] or 0,
            }
            for r in self.env.cr.fetchall()
        ]
