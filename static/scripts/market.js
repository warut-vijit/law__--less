var app = angular.module('marketApp', []);
app.controller('marketCtrl', function($scope, $http) {
    $scope.dev = "The devs are awesome!";
    $scope.extensions = "not done loading";
    $http.get("/market/getextensions")
    .then(function(response) {
        console.log("response received");
        $scope.extensions = response.data;
    }, function(response) {
        //Second function handles error
        console.log("error");
        $scope.extensions = "Something went wrong";
    });
});