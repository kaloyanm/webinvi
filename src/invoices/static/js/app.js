// Define the `invoiceApp` module
var invoiceApp = angular.module('invoiceApp', []);
    invoiceApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

// Define the `InvoiceItemsController` controller on the `invoiceApp` module
invoiceApp.controller('InvoiceItemsController', function InvoiceItemsController($scope) {
    $scope.items = window.invoice_details;
    $scope.add = function () {
        $scope.items.push({});
    };
    $scope.remove = function (index) {
        $scope.items.splice(index, 1);
    };
});
