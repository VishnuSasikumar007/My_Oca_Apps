/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class PosDashboard extends Component {

    setup(){

        this.orm = useService("orm");

        this.state = useState({
            sales: 0,
            products: [],
            stores: [],
            payments: [],
            customers: [],

            sessions: [],
            all_sessions: [],

            total_order_count: 0,
            filter: "today",
            selected_session: null,

            notifications: [],
            notification_count: 0,
            showNotifications: false,

            user: {},
            current_datetime: "",

            dark_mode: localStorage.getItem("pos_dashboard_theme") === "dark",

            showSessionPopup: false,
            showProductPopup: false,
            showStoreRankingPopup: false,

            showProductDetails: false,
            product_details: [],

            store_ranking: [],
            showProductChart: false,
            showStorePopup: false,
            categories: [],
            showCategoryPopup: false,
            category_products: [],
            showCategoryProducts: false,
            currency: {},
            showStoreChart:false,
            open_sessions: 0,
            closed_sessions: 0,
            activity_feed: [],
            store_comparison: [],
            showCustomerPopup: false,
            filtered_products: [],
            top_cashiers: [],
            showCashierPopup: false,

            showPaymentPopup: false,
            paymentDetails: [],
            selectedPaymentMethod: "",
            has_new_orders: false,
            latest_order_id: 0,
            sidebar_open: false,
            showAboutPopup: false,
            selected_product: null,

        });

        onWillStart(async () => {
            await this.loadDashboard();

            setInterval(async () => {
                await this.checkNewOrders();
            }, 10000); // every 10 seconds
        });

    }


// ==============================
// THEME TOGGLE
// ==============================

    toggleTheme(){

        this.state.dark_mode = !this.state.dark_mode;

        if (this.state.dark_mode){
            localStorage.setItem("pos_dashboard_theme","dark");
        }else{
            localStorage.setItem("pos_dashboard_theme","light");
        }

    }

// toggle for store performance pie chart

    toggleStoreChart(){

        this.state.showStoreChart = !this.state.showStoreChart;

        if(this.state.showStoreChart){
            setTimeout(()=>{
                this.renderStoreChart();
            },100);
        }

    }

toggleSidebar() {
    this.state.sidebar_open = !this.state.sidebar_open;
}
// ==============================
// LOAD DASHBOARD DATA
// ==============================
    async loadDashboard(){

        const data = await this.orm.call(
    "pos.sales.dashboard",
    "get_dashboard_data",
    [
        this.state.filter,
        this.state.selected_session,
        this.state.selected_product,
        this.state.selected_store,
        this.state.selected_category_filter,
        this.state.selected_cashier,
        this.state.selected_payment_filter,
    ]
);

        this.state.sales = data.total_sales;
        this.state.products = data.products;
        this.state.stores = data.stores;
        this.state.total_order_count = data.total_order_count;
        this.state.payments = data.payments;
        this.state.customers = data.customers;
        this.state.store_ranking = data.store_ranking || [];

        this.state.sessions = data.sessions;
        this.state.all_sessions = data.all_sessions;

        this.state.user = data.user;

        this.state.notifications = data.notifications || [];
        this.state.notification_count = data.notification_count || 0;
        this.state.categories = data.categories || [];
        this.state.currency = data.currency || {};
        this.state.open_sessions = data.open_sessions || 0;
        this.state.closed_sessions = data.closed_sessions || 0;
        this.state.store_comparison = data.store_comparison || [];
        this.state.filtered_products = data.products;
        this.state.top_cashiers = data.top_cashiers || [];

        this.state.all_products = data.all_products || [];
this.state.all_stores = data.all_stores || [];
this.state.all_categories = data.all_categories || [];
this.state.all_cashiers = data.all_cashiers || [];
this.state.all_payment_methods = data.all_payment_methods || [];

        if (!this.state.latest_order_id) {
    this.state.latest_order_id = await this.orm.call(
        "pos.sales.dashboard",
        "get_latest_order_id",
        []
    );
}
        

// render charts if enabled
        setTimeout(()=>{

            if(this.state.showProductChart){
                this.renderProductChart();
            }

            if(this.state.showStoreChart){
                this.renderStoreChart();
            }

            this.renderStoreComparisonChart();

        },50);




    }


// ==============================
// CHECK NEW ORDER
// ==============================


   async checkNewOrders() {

    const latest_id = await this.orm.call(
        "pos.sales.dashboard",
        "get_latest_order_id",
        []
    );

    if (latest_id > this.state.latest_order_id) {
        this.state.has_new_orders = true;
    }
}

// ==============================
// REFRESH METHOD
// ==============================

async refreshDashboard() {
    await this.loadDashboard();

    this.state.has_new_orders = false;

    this.state.latest_order_id = await this.orm.call(
        "pos.sales.dashboard",
        "get_latest_order_id",
        []
    );
}

// ==============================
// FILTER BUTTONS
// ==============================

    async changeFilter(ev){

        const filter = ev.currentTarget.dataset.filter;

        this.state.filter = filter;

        await this.loadDashboard();

    }




// load activity feed

    async loadActivityFeed(){

        const data = await this.orm.call(
            "pos.sales.dashboard",
            "get_activity_feed",
            []
            );

        this.state.activity_feed = data;

    }


// ==============================
// SESSION CHANGE
// ==============================

    async changeSession(ev){

        const value = ev.target.value;

        if(!value){
            this.state.selected_session = null;
        }else{
            this.state.selected_session = parseInt(value);
        }

        await this.loadDashboard();

    }

// ==============================
// NOTIFICATIONS
// ==============================

    toggleNotifications(){
        this.state.showNotifications = !this.state.showNotifications;
    }

    async markNotificationsRead(){

        await this.orm.call(
            "pos.sales.dashboard",
            "mark_notifications_read",
            []
            );

        this.state.notifications = [];
        this.state.notification_count = 0;
        this.state.showNotifications = false;

    }


// ==============================
// SESSION POPUP
// ==============================

    openSessionPopup(){
        this.state.showSessionPopup = true;
    }

    closeSessionPopup(){
        this.state.showSessionPopup = false;
    }


// ==============================
// PRODUCT POPUP
// ==============================

    openProductPopup(){
        this.state.showProductPopup = true;
    }

    closeProductPopup(){
        this.state.showProductPopup = false;
    }


// ==============================
// STORE RANKING POPUP
// ==============================

    openStoreRankingPopup(){
        this.state.showStoreRankingPopup = true;
    }

    closeStoreRankingPopup(){
        this.state.showStoreRankingPopup = false;
    }

// ==============================
// Cashier Ranking Popup
// ==============================

    openCashierPopup() {
        this.state.showCashierPopup = true;
    }

    closeCashierPopup() {
        this.state.showCashierPopup = false;
    }


// ==============================
// PRODUCT DETAILS
// ==============================

    async openProductDetails(ev){

        const productId = parseInt(ev.currentTarget.dataset.product);

        const details = await this.orm.call(
            "pos.sales.dashboard",
            "get_product_sales_details",
            [
                productId,
                this.state.filter,
                this.state.selected_session
            ]
            );

        this.state.product_details = details;
        this.state.showProductDetails = true;

    }

    closeProductDetails(){
        this.state.showProductDetails = false;
    }

// customer open popup
    openCustomerPopup() {
        this.state.showCustomerPopup = true;
    }
// customer close popup

    closeCustomerPopup() {
        this.state.showCustomerPopup = false;
    }

// About popup
    openAboutPopup() {
    this.state.showAboutPopup = true;
}

closeAboutPopup() {
    this.state.showAboutPopup = false;
}


// ==============================
// PRODUCT CHART TOGGLE
// ==============================

    toggleProductChart(){

        this.state.showProductChart = !this.state.showProductChart;

        if(this.state.showProductChart){
            setTimeout(()=>{
                this.renderProductChart();
            },100);
        }

    }





// Search Function

    onProductSearch(ev) {
        const query = ev.target.value.toLowerCase();

        if (!query) {
            this.state.filtered_products = this.state.products;
            return;
        }

        this.state.filtered_products = this.state.products.filter(p =>
            p[0].toLowerCase().includes(query)
            );
    }

// category related product popup

    async openCategoryProducts(ev){

        const categoryId = parseInt(ev.currentTarget.dataset.category);

        const products = await this.orm.call(
            "pos.sales.dashboard",
            "get_category_products",
            [
                categoryId,
                this.state.filter,
                this.state.selected_session
            ]
            );

        this.state.category_products = products;
        this.state.showCategoryProducts = true;

    }


// ==============================
// STORE POPUP
// ==============================

    openStorePopup(){
        this.state.showStorePopup = true;
    }

    closeStorePopup(){
        this.state.showStorePopup = false;
    }

// product categories

    openCategoryPopup(){
        this.state.showCategoryPopup = true;
    }

    closeCategoryPopup(){
        this.state.showCategoryPopup = false;
    }

// category related product close popup
    closeCategoryProducts(){
        this.state.showCategoryProducts = false;
    }


// ==============================
// PRODUCT BAR CHART
// ==============================

// Top selling products bar chart

    renderProductChart(){

        const canvas = document.getElementById("productChart");
        if(!canvas) return;

        const ctx = canvas.getContext("2d");

        if(this.productChart){
            this.productChart.destroy();
        }

        const products = this.state.products.slice(0,5);

        const labels = products.map(p => p[0]);
        const qtyValues = products.map(p => p[1]);

// total sales amount
        const amountValues = products.map(p => p[3] || 0);

        this.productChart = new Chart(ctx,{
            type:"bar",
            data:{
                labels:labels,
                datasets:[{
                    label:"Qty Sold",
                    data:qtyValues,
                    backgroundColor:[
                        "#4e73df",
                        "#1cc88a",
                        "#f6c23e",
                        "#e74a3b",
                        "#36b9cc"
                    ],
                    borderRadius:6,
                    barPercentage:0.6,
                    categoryPercentage:0.6
                }]
            },
            options:{
                responsive:true,
                maintainAspectRatio:false,

                plugins:{
                    legend:{
                        display:false
                    },

                    tooltip:{
                        callbacks:{
                            label:(context)=>{
                                const qty = context.raw;
                                const amount = amountValues[context.dataIndex] || 0;

                                return [
                                    "Qty Sold : " + qty,
                                    "Sales : " + this.state.currency.symbol + amount.toLocaleString()
                                ];
                            }
                        }
                    }

                },

                scales:{

                    x:{
                        ticks:{
                            color:this.state.dark_mode ? "#e5e7eb" : "#333",
                            autoSkip:false,
                            maxRotation:45,
                            minRotation:30,
                            font:{size:10}
                        },
                        grid:{
                            display:false
                        }
                    },

                    y:{
                        beginAtZero:true,
                        ticks:{
                            color:this.state.dark_mode ? "#e5e7eb" : "#333",
                            font:{size:10}
                        },
                        grid:{
                            color:this.state.dark_mode ? "#334155" : "#e5e7eb"
                        }
                    }

                }

            }
        });

    }

// Store performance pie chart

    renderStoreChart(){

        const canvas = document.getElementById("storeChart");
        if(!canvas) return;

        const ctx = canvas.getContext("2d");

        if(this.storeChart){
            this.storeChart.destroy();
        }

        const stores = this.state.stores.slice(0,5);

        const labels = stores.map(s => s[0]);
        const values = stores.map(s => s[2]);

        this.storeChart = new Chart(ctx,{
            type:"pie",
            data:{
                labels:labels,
                datasets:[{
                    data:values,
                    backgroundColor:[
                        "#4e73df",
                        "#1cc88a",
                        "#f6c23e",
                        "#e74a3b",
                        "#36b9cc"
                    ],
                    borderWidth:1,
                    borderColor:this.state.dark_mode ? "#0f172a" : "#ffffff"
                }]
            },
            options:{
                responsive:true,
                maintainAspectRatio:false,

                plugins:{

                    legend:{
                        position:"bottom",
                        labels:{
                            color:this.state.dark_mode ? "#e5e7eb" : "#333",
                            font:{
                                size:12
                            }
                        }
                    },

                    tooltip:{
                        callbacks:{
                            label:(context)=>{
                                return context.label + " : " +
                                this.state.currency.symbol +
                                context.raw.toLocaleString();
                            }
                        }
                    }

                }
            }
        });

    }

// Comparison Chart Render

    renderStoreComparisonChart(){

        const canvas = document.getElementById("storeComparisonChart");
        if(!canvas) return;

        const ctx = canvas.getContext("2d");

        if(this.storeComparisonChart){
            this.storeComparisonChart.destroy();
        }

        const data = this.state.store_comparison;

        const labels = data.map(s => s.store);
        const current = data.map(s => s.current);
        const previous = data.map(s => s.previous);

        this.storeComparisonChart = new Chart(ctx,{
            type:"bar",
            data:{
                labels:labels,
                datasets:[
                    {
                        label:"Current Period",
                        data:current,
                        backgroundColor:"#4e73df"
                    },
                    {
                        label:"Previous Period",
                        data:previous,
                        backgroundColor:"#f59e0b"
                    }
                ]
            },
            options:{
                responsive:true,
                maintainAspectRatio:false,
                plugins:{
                    legend:{
                        position:"bottom"
                    }
                },
                scales:{
                    y:{
                        beginAtZero:true
                    }
                }
            }
        });
    }


    // Payment details
    async openPaymentDetails(ev){

        const paymentMethod = ev.currentTarget.dataset.payment;

        const details = await this.orm.call(
            "pos.sales.dashboard",
            "get_payment_method_details",
            [
                paymentMethod,
                this.state.filter,
                this.state.selected_session
            ]
        );

        this.state.paymentDetails = details;
        this.state.selectedPaymentMethod = paymentMethod;
        this.state.showPaymentPopup = true;
    }

    closePaymentPopup(){
        this.state.showPaymentPopup = false;
}




}

PosDashboard.template = "pos_sales_dashboard.Template";
registry.category("actions").add("pos_dashboard",PosDashboard);
