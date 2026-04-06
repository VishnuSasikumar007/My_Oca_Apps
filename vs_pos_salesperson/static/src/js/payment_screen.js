/** @odoo-module **/

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { SelectionPopup } from "@point_of_sale/app/components/popups/selection_popup/selection_popup";
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { ask, makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";

patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
    },

    async selectSalespersonView(selectionList) {
        const payload = await makeAwaitable(this.dialog, SelectionPopup, {
            title: _t("Change Salesperson"),
            list: selectionList,
        });

        if (!payload) {
            return false;
        }

        return payload;
    },

    async validateOrder(isForceValidate = false) {

        const order = this.currentOrder;
        if (this.pos.config.salesperson_compulsory && !order.get_salesperson()) {
            this.dialog.add(AlertDialog, {
                title: "Missing Salesperson",
                body: "Please select a salesperson before validating the order.",
            });
            return;
        }
        await super.validateOrder(isForceValidate);
    },

    async selectSalesperson() {

        let salespeople = null;

    // 1. Check from selected order
        if (this.pos.selectedOrder && this.pos.selectedOrder.salespeople) {
            salespeople = this.pos.selectedOrder.salespeople;
        } else {

            let salespersonIds = [];
            const raw = this.pos.config.salesperson_ids;

        // 2. Normalize IDs (VERY IMPORTANT)
            if (Array.isArray(raw)) {
                if (raw.length && Array.isArray(raw[0]) && raw[0][0] === 6) {
                // many2many command format
                    salespersonIds = raw[0][2];
                } else {
                    salespersonIds = raw.map(sp =>
                        typeof sp === "number" ? sp :
                        Array.isArray(sp) ? sp[0] :
                        typeof sp === "object" ? sp.id :
                        sp
                        );
                }
            }

        // 3. Fetch from backend
            if (salespersonIds.length > 0) {
                salespeople = await this.pos.data.orm.call(
                    'hr.employee',
                    'search_read',
                    [
                        [['id', 'in', salespersonIds]],
                        ['id', 'name']
                    ]
                    );
            }
        }

    // 4. UI Handling
        if (salespeople && salespeople.length > 0) {
            const list = salespeople.map((sp) => ({
                id: sp.id,
                item: sp,
                label: sp.name,
                isSelected: false,
            }));

            const sales_person = await this.selectSalespersonView(list);

            if (sales_person) {
                this.pos.set_salesperson(sales_person);
                return { name: "PaymentScreen" };
            }

        } else {
            console.error("Error: Salespeople not found.");
            return this.pos.dialog.add(AlertDialog,  {
                title: _t("Warning"),
                body: _t('Salespeople not found !'),
            });
        }
    }

})


