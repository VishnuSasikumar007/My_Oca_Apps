/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { jsonrpc } from "@web/core/network/rpc_service";


patch(PosStore.prototype, {

    async addProductToCurrentOrder(product, options = {}) {

        let quant = await jsonrpc("/web/dataset/call_kw/product.product/action_get_warehouse_quant", {
            model: 'product.product',
            method: 'action_get_warehouse_quant',
            args: [product.id, this.config.id],
            kwargs: {}
        });

        // Get current order
        const order = this.get_order();

        // Find existing line for same product
        let line = order.get_orderlines().find(l => l.product.id === product.id);

        let qty_in_order = 0;
        if (line) {
            qty_in_order = line.get_quantity();
        }

        // Remaining stock check
        if ((quant - qty_in_order) <= 0) {
            const message = `Only ${quant} quantity available for - ${product.display_name}`;

            this.env.services.popup.add(ErrorPopup, {
                title: _t("Stock Not Available"),
                body: _t(message),
            });
            return;
        }

        return super.addProductToCurrentOrder(...arguments);
    }

})



