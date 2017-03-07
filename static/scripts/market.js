var app = angular.module('marketApp', []);
app.controller('marketCtrl', function($scope, $http) {
    var position = 0;
    var total_extensions = 0;
    $scope.extensions = "";

    //initialize list
    get_batch(0);
    
    $scope.previous_batch = function() {
        position = Math.max(position-10, 0);
    }
    $scope.next_batch = function() {
        position = Math.min(position+10, total_extensions);
    }

    // helper functions
    $scope.select_all = function() {
        alert("selecting");
        document.getElementsByClassName("checkbox").forEach(function(element){
            element.value = true;
        });
    }

    // backend calls
    function get_batch(offset) {
        $http.get("/market/getextensions")
        .then(function(response) {
            console.log("response received: "+response.data);
            $scope.extensions = response.data;
        }, function(response) {
            //Second function handles error
            console.log("error fetching extensions");
        });
    }
    function get_total_extensions() {
        $http.get("/market/countextensions")
        .then(function(response) {
            console.log("response received: "+response.data);
            total_extensions = response.data;
        }, function(response) {
            //Second function handles error
            console.log("error fetching extensions");
        });
    }
});