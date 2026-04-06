/** @odoo-module **/

import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";

patch(PosOrder.prototype, {

    setup(vals) {
        super.setup(vals);

        this.salesperson = false;
        if (this.uiState && this.uiState.salesperson) {
            this.salesperson = this.uiState.salesperson;
        }
        if (!this.salesperson && vals.salesperson_id) {
            this.salesperson = {
                id: Array.isArray(vals.salesperson_id)
                    ? vals.salesperson_id[0]
                    : vals.salesperson_id,
                name: Array.isArray(vals.salesperson_id)
                    ? vals.salesperson_id[1]
                    : "Salesperson",
            };
        }

        // Sync UI state
        if (this.uiState) {
            this.uiState.salesperson = this.salesperson;
        }
    },

    initState() {
        super.initState();

        if (!this.uiState.salesperson) {
            this.uiState.salesperson = false;
        }
    },

    serializeForORM(opts = {}) {
        const data = super.serializeForORM(opts);

        data.salesperson_id = this.salesperson
            ? this.salesperson.id
            : false;

        return data;
    },

    set_salesperson(salesperson) {
        this.salesperson = salesperson || false;

        if (this.uiState) {
            this.uiState.salesperson = this.salesperson;
        }
    },

    get_salesperson() {
        return this.salesperson;
    },

    get_salesperson_name() {
        return this.salesperson ? this.salesperson.name : "";
    },

});