import Vue from 'vue';

var round = function (number, precision) {
  var factor = Math.pow(10, precision);
  var tempNumber = number * factor;
  var roundedTempNumber = Math.round(tempNumber);
  return roundedTempNumber / factor;
};

var app = new Vue({
  el: "#invoice-container",
  data: {
    rows: [],
    currencies: [],
    selected_currency: 'BGN',
    current_rate: 1,
    total_forms: 0,
    initial_forms: 0,
    total: 0,
    gross: 0,
    dds_percent: 0
  },
  mounted: function () {
    this.rows = window.formset.map(function(row){ return row });
    for(var row_idx in this.rows) {
      var row = this.rows[row_idx];
      row.unit_price_original = row.unit_price;
    };
    this.currencies = Object.keys(window.EXCHANGE_RATES);
    if (this.rows.length == 0) {
      this.add();
    }

    this.calc_total(true);
    this.total_forms = this.rows.length;
  },
  methods: {
    add: function () {
      this.rows.push({name: "", quantity: 1, unit: "", unit_price:0, discount: "", gross: 0, id: 0});
      this.total_forms = this.rows.length;
    },

    remove: function (index) {
      this.rows.splice(index, 1);
      if (this.rows.length == 0) {
        this.add();
      }

      this.total_forms = this.rows.length;
      this.calc_total()
    },

    add_empty: function (index) {
      if (index == this.rows.length - 1) {
        this.add();
      }
      this.total_forms = this.rows.length;
    },

    calc_row: function (index) {
      var row = this.rows[index];
      console.log(JSON.stringify(row));
      row.gross = round(row.unit_price * row.quantity, 2);

      if (row.discount) {
        row.gross = row.gross - row.gross * row.discount / 100;
      }
      console.log(JSON.stringify(row));
      this.rows[index] = row;
    },

    calc_total: function (force_update_rows) {
      force_update_rows = force_update_rows || false;
      this.gross = 0;
      for (var i = 0; i < this.rows.length; i++) {
        if (force_update_rows) {
          this.calc_row(i);
        }
        var row = this.rows[i];
        this.gross = this.gross + row.gross;
      }

      if (this.dds_percent) {
        this.total = this.gross + this.gross * this.dds_percent / 100;
      } else {
        this.total = this.gross;
      }
    },

    unit_price_changed: function(index) {
      var row = this.rows[index];
      row.unit_price_original = row.unit_price;
    },

    update_unit_prices: function(){
      var r = this.current_rate;
      for(var row_idx in this.rows) {
        var row = this.rows[row_idx];
        if(row.unit_price_original == null || row.unit_price_original == undefined) {
          continue;
        }
        row.unit_price = row.unit_price_original * r;
      }
      this.calc_total(true);
    },

    currency_selected: function (selected_currency){
      this.current_rate = EXCHANGE_RATES[selected_currency];
      this.update_unit_prices();
    },

    rate_changed: function() {
      this.update_unit_prices();
    }
  }
});
