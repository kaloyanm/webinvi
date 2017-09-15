import Vue from 'vue';

var round = function (number, precision) {
  var factor = Math.pow(10, precision);
  var tempNumber = number * factor;
  var roundedTempNumber = Math.round(tempNumber);
  return roundedTempNumber / factor;
};

var app = new Vue({
  el: "#invoice_app",
  data: {
    rows: [],
    total_forms: 0,
    initial_forms: 0,
    total: 0,
    gross: 0,
    dds_percent: 0
  },
  mounted: function () {
    this.rows = window.formset;
    if (this.rows.length == 0) {
      this.add();
    }

    this.calc_total(true);
  },
  methods: {
    add: function () {
      this.rows.push({name: "", quantity: 1, unit: "", unit_price: 0, discount: "", gross: 0, id: 0});
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
      row.gross = round(row.unit_price * row.quantity, 2);

      if (row.discount) {
        row.gross = row.gross - row.gross * row.discount / 100;
      }
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
    }
  }
});
