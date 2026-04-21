/** @odoo-module */
import { _t } from "@web/core/l10n/translation";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { useRef,useState} from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { session } from "@web/session";
import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

export class SendStockPopup extends Component {
    static template = "pos_internal_stock_transfer.SendStockPopup";
    static components = { Dialog };

    static props = {
        title: { type: String, optional: true },
        configName: String,
        pickingData: Array,
        warehouses: Array,
        close: Function,  
        getPayload: { type: Function, optional: true }
    };

    setup() {
        this.pos = usePos();
        this.orm = useService("orm");
        this.dialog = useService("dialog");
        this.state = useState({
            wareValue: "",
        });
    }

    static defaultProps = {
        confirmText: _t("Confirm"),
        cancelText: _t("Discard"),
        clearText: _t("Clear"),
        title: "",
        body: "",
    };

    async action_confirm() {
        if (!this.state.wareValue) {
            return this.pos.dialog.add(AlertDialog,  {
                title: _t("Access Denied"),
                body: _t('Please select the sent to location.'),
            });
        }
        const res = await this.orm.call("pos.config", "action_send_stock", [[this.pos.config.id], this.props.pickingData, this.state.wareValue], {});
        if (res) {
            const transfer = this.pos.dialog.add(AlertDialog,  {
                title: _t('Transfer Created'),
                body: _t(res),
        });
         return { name: "ProductScreen" };
     }

     this.cancel();
 }


 action_cancel() {
    this.props.close(null);
}




}




