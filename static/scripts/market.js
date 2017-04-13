var app = angular.module('marketApp', []);
app.controller('marketCtrl', function($scope, $http) {
    $scope.position = 0;
    $scope.total_extensions = 0;
    $scope.extensions = "";
    $scope.expanded_ext;
    $scope.expand = false;
    $scope.upload_active = false;

    //initialize list
    get_batch(0);
    get_total_extensions();
    
    $scope.previous_batch = function() {
        $scope.position = Math.max($scope.position-10, 0);
        get_batch($scope.position)
        console.log("Backtracked to position "+$scope.position)
    }
    $scope.next_batch = function() {
        $scope.position = Math.min($scope.position+10, $scope.total_extensions);
        get_batch($scope.position)
        console.log("Advanced to position "+$scope.position)
    }
    $scope.vote = function(extension, value) {
        extension.rating_points += value;
        extension.total_ratings += 1; // add vote
        put_vote(extension["id"], extension.rating_points, extension.total_ratings);
        console.log("Vote submitted, value set to "+rating_points);    
    }
    $scope.expand_ext = function(extension) {
        $scope.expanded_ext = extension;
        $scope.expand = true;
    }
    $scope.close_ext = function() {
        console.log("Closing menu");
        $scope.expanded_ext = "";
        $scope.expand = false;
        $scope.upload_active = false;
    }
    $scope.upload_ext = function() {
        $scope.upload_active = true;
    }

    // helper functions
    $scope.select_all = function() {
        var checkboxes = document.getElementsByClassName("checkbox");
        for(var index = 0; index<checkboxes.length; index++){
            checkboxes[index].checked = true;
        }
    }
    $scope.end_batch = function() {
        return Math.min($scope.position+10, $scope.total_extensions)
    }

    // backend calls
    function get_batch(offset) {
        $http({
            url: "/market/getextensions",
            method: "GET",
            params: {offset: offset}
        })
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
            $scope.total_extensions = response.data;
        }, function(response) {
            //Second function handles error
            console.log("error counting extensions");
        });
    }
    function put_vote(id, rating_points, total_ratings) {
        $http({
            url: "/market/vote",
            method: "GET",
            params: {id: id, rating_points: rating_points, total_ratings: total_ratings}
        })
        .then(function(response){
            console.log("successfully voted for extension id "+id);
        }, function(response){
            console.log("error occurred while voting");
        });
    }
});