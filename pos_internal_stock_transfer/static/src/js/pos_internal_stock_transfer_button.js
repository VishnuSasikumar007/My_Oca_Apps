/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { SendStockPopup } from "./pos_internal_stock_transfer_popup";
import { _t } from "@web/core/l10n/translation";

patch(ControlButtons.prototype, {

    setup() {
        super.setup();
        this.pos = usePos();
        this.dialog = useService("dialog");
        this.orm = useService("orm");
    },

    async onClickSendStock() {
        let currentOrder = this.pos.getOrder();
        var order = this.pos.selectedOrder
        let orderLines = currentOrder.getOrderlines();

        let pickingData = orderLines.map(line => ({ pid: line.getProduct().id, qty: line.getQuantity() }));
        if (orderLines.length > 0) {
            var self = this
            configName:this.pos.config.name
            pickingData:pickingData
            let warehouses = await this.orm.call(
                "stock.picking", "action_get_warehouses", [], {}
                )
            this.dialog.add(SendStockPopup, {
                title: _t("Stock Transfer"),
                configName:this.pos.config.name,
                pickingData:pickingData,
                warehouses:warehouses

            });

        }else{
            return this.pos.dialog.add(AlertDialog,  {
                title: "Warning",
                body: "Please add products to preceed.",
            });
        }
    }

});