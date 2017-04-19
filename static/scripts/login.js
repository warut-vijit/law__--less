var app = angular.module('loginApp', []);
app.controller('loginCtrl', function($scope, $http) {
    $scope.loginActive = false;
    $scope.showLoginWindow = false;
    $scope.showSignupWindow = false;
    $scope.summaryActive = false;
    $scope.summary = "";

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

    // Special functions for cases
    $scope.get_extensions = function() {
        $http({
            url: "/market/getextensions/",
            method: "GET"
        }).then(function(response){
            //console.log("Successfully fetched "+reponse.length+" extensions.");
            $scope.extensions = response.data;
            console.log($scope.extensions);
        }, function(error){
            console.log("Error occurred while fetching extensions.");
        });
    }

    $scope.query_summary = function($event) {
        if($event.key=="Enter"){
            $http({
                url: "/cases",
                method: "POST",
                params: {
                    query: document.getElementById("query").value 
                }
            }).then(function(response){
                //TODO: Update hierarchy with response data
                document.getElementById("query").value = "";
                document.getElementById("query").style.borderLeft = "3px solid var(--scarlet)";
                setTimeout(function(){
                    document.getElementById("query").style.borderLeft = "3px solid var(--darkblue)";
                    document.getElementById("main").focus();
                }, 500);
                console.log("Successfully queried summary.");
            }, function(error){
                console.log("Error occurred while querying summary.");
            });
        }
    }

    $scope.get_target = function() {
        $http({
            url: "/get-target",
            method: "GET",
        }).then(function(response){
            if(response.data!=""){
                console.log(response.data);
                $scope.summaryActive = true;
                $scope.summary = encryptxor("imaginecup2017", response.data);
            }
        }, function(error){
            console.log("Error occurred while retrieving summary.");
        });
    }

    $scope.download_summary = function() {
        if($scope.summaryActive) {
            var link = document.createElement("a");
            link.href = 'data:text/plain;charset=utf-8,' + $scope.summary;
            link.download = "law--less.txt";
            link.click();
        }
    }

    function encryptxor (key, message) {
        var message_out = "";
        for(var x=0; x<message.length; x++){
            message_out += String.fromCharCode(message.charCodeAt(x) ^ key.charCodeAt(x%key.length));
        }
        return message_out;
    }

});