import Vue from 'vue';
import $ from 'jquery';

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
    total_forms: 0,
    initial_forms: 0,
    total: 0,
    gross: 0,
    dds_percent: window.INVOICE_DDS_DEFAULT
  },
  mounted: function () {
    this.rows = window.INVOICE_ITEMS.map(function(row){ return row });
    for(var row_idx in this.rows) {
      var row = this.rows[row_idx];
      row.unit_price_original = row.unit_price;
    };
    if (this.rows.length == 0) {
      this.add();
    }

    this.total_forms = this.rows.length;
    this.initial_forms = this.rows.length;
    this.calc_total(true);
  },
  methods: {
    add: function () {
      this.rows.push($.extend({}, window.INVOICE_ITEM_TEMPLATE));
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
      row.gross = row.unit_price * row.quantity;

      if (row.discount) {
        row.gross = row.gross - row.gross * row.discount / 100;
      }
      row.gross = round(row.gross, 2)
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
        this.total = round(this.gross + this.gross * this.dds_percent / 100, 2);
      } else {
        this.total = round(this.gross, 2);
      }
    },

    unit_price_changed: function(index) {
      var row = this.rows[index];
      row.unit_price_original = row.unit_price;
    }
  }
});
