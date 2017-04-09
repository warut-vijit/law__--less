var app = angular.module('loginApp', []);
app.controller('loginCtrl', function($scope, $http) {
    $scope.loginActive = false;
    $scope.showLoginWindow = false;
    $scope.showSignupWindow = false;

    $scope.cases = [{name:"Jean Valjean"}, {name:"Marius Pontmercy"}, {name:"Gavroche"}, {name:"Javert"}];

    $scope.get_credentials = function() {
        $http.get("/login/getcredentials")
        .then(function(response) {
            if(response.data == ""){  // Not logged in
                $scope.loginActive = false;
            }
            else{
                $scope.loginActive = true;
                $scope.user = response.data;
                $scope.user_since_formatted = $scope.user.since.replace(/00:00:00.*/, '');
                $scope.user_ends_formatted = $scope.user.ends.replace(/00:00:00.*/, '');
            }
            console.log("response received: "+response.data);
        }, function(response) {
            console.log("Error acquiring credentials.");
        });
    };

    $scope.get_credentials();

    $scope.login = function() {
        console.log("Login window open");
        $scope.showLoginWindow = true;
        $scope.showSignupWindow = false;
    };

    $scope.show_signup = function() {
        console.log("Signup window open");
        $scope.showSignupWindow = true;
        $scope.showLoginWindow = false;
    }

    $scope.close_ext = function() {
        console.log("Closing window");
        $scope.showLoginWindow = false;
        $scope.showSignupWindow = false;
    };

    $scope.verify = function() {
        $scope.showSignupWindow = false;
        $http({
            url: "/login/verify",
            method: "GET",
            params: {
                username: document.getElementById("username").value, 
                password: document.getElementById("password").value
            }
        })
        .then(function(response) {
            console.log("response received: "+response.data);
            if(response.data=="fail"){
                $scope.showFailMessage = true;
            }
            else{
                $scope.showLoginWindow = false;
                $scope.get_credentials();
            }
        }, function(response) {
            //Second function handles error
            console.log("Error verifying login information.");
        });
    };

    $scope.signup = function() {
        $scope.showSignupWindow = false;
        $http({
            url: "/login/signup",
            method: "GET",
            params: {
                name: document.getElementById("name").value,
                username: document.getElementById("username").value, 
                password: document.getElementById("password").value
            }
        })
        .then(function(response) {
            console.log("response received: "+response.data);
            if(response.data=="fail"){
                $scope.showFailMessage = true;
            }
            else{
                $scope.showSignupWindow = false;
                $scope.get_credentials();
            }
        }, function(response) {
            //Second function handles error
            console.log("Error creating an account.");
        });
    };

});