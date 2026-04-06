/** @odoo-module */

import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";

patch(PosStore.prototype, {

        get_salesperson (){
            var order = this.getOrder();
            if (order) {
                return order.get_salesperson();
            }
            return null;
        },

        set_salesperson (salesperson) {
            var order = this.getOrder();
            if (order) {
                return order.set_salesperson(salesperson);
            }
            return null;
        },

    });
