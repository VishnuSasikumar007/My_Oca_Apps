/** @odoo-module **/
import { ProductConfiguratorPopup } from "@point_of_sale/app/components/popups/product_configurator_popup/product_configurator_popup";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";

patch(ProductScreen.prototype, {
    setup() {
            super.setup();
            this.action = useService("action");
            this.orm = useService("orm");
    },

    // Raise the waring if product have no stock while click the product with no variants
    async addProductToOrder(product) {

            if (product.raw.attribute_line_ids.length === 0 ){
                const stock_quant = await this.orm.call("product.template","tmp_action_get_warehouse_quant",[product.id,this.pos.config.id])
                if (stock_quant <= 0) {
                const message = `The selected product has no stock, so please update it and proceed with the order for - ${product.display_name}.`;
                    this.dialog.add(AlertDialog, {
                            title: _t("Access Denied"),
                            body: _t(message),
                    });
                return
            }
            }
            await super.addProductToOrder(product);

    },
    // Raise the warning if product does not have any stock while scan using barcode.  
    async _barcodeProductAction(code) {

        const product = await this._getProductByBarcode(code);

        if (!product) {
            this.sound.play("error");
            this.barcodeReader.showNotFoundNotification(code);
            return;
        }

        // Check stock BEFORE adding
        const stock_quant = await this.pos.data.call(
            "product.product",
            "action_get_warehouse_quant_prod",
            [product.id, this.pos.config.id]
        );

        if (stock_quant <= 0) {

            const message = `The selected product has no stock, please update stock for - ${product.display_name}.`;

            this.pos.dialog.add(AlertDialog, {
                title: _t("Access Denied"),
                body: _t(message),
            });

            return; //product will NOT be added
        }

        //Only call super if stock is valid
        return await super._barcodeProductAction(...arguments);
}

     
})

// overide the base method to raise the warning in product popup if product dont have any stock based on the location if product have variants

patch(ProductConfiguratorPopup.prototype, {
    async confirm() {
        const payload = this.computePayload();
        const selected = payload.attribute_value_ids;
        const templateId = this.props.productTemplate.id;

        const pos = this.env.services.pos;

        const allProducts = [...pos.models["product.product"].records.values()];

        const variants = allProducts.filter(
            p => p.product_tmpl_id === templateId ||
                 p.product_tmpl_id?.raw?.id === templateId
        );

        const variant = variants.find(v => {

            const variantValueIds = [...v.product_template_variant_value_ids]
                .map(val => val.id || val.raw?.id);

            return selected.length === variantValueIds.length &&
                   selected.every(id => variantValueIds.includes(id));
        });

        if (variant?.id) {
            const stock_quant = await this.pos.data.call(
                "product.product",
                "action_get_warehouse_quant_prod",
                [variant.id, pos.config.id]
            );

            if (stock_quant <= 0) {

                const message = `The selected product has no stock, so please update it and proceed with the order for - ${variant.display_name}.`;

                this.pos.dialog.add(AlertDialog, {
                    title: _t("Access Denied"),
                    body: _t(message),
                });

                return; // stop here
            }
        }

        // Proceed normally
        this.props.getPayload(payload);
        this.props.close();
    },


});





