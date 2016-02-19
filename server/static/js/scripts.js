(function(){
    'use strict';
var app = angular.module('myApp', ['authentication'], function config($httpProvider){
        $httpProvider.interceptors.push('AuthInterceptor');
    });
app.controller('myCtrl', function($scope, $http, UserFactory, API_URL){
    'use strict';


    // user aouthorization block
    // ======================================================================
    $scope.login = login;
    $scope.logout = logout;
    $scope.register = register;
    $scope.user_error = 'Error! ';

    // initialization
    UserFactory.verifyUser().then(function success(response){
        $scope.user = response.data;
    });


    $scope.signInForm = true;
    $scope.signUpForm = false;
    $scope.sign_link = 'Sign Up';
    $scope.setForm = setForm;

    function setForm(){
        $scope.signInForm = !$scope.signInForm;
        $scope.signUpForm = !$scope.signUpForm;
        if ($scope.signInForm){
            $scope.sign_link = 'Sign Up';
        }else{
            $scope.sign_link = 'Sign In';
        }

    }

    function login(username, password){
        UserFactory.login(username, password).then(function success(response){
            $scope.user = response.data.user;
        }, handleError);
    }

    function logout(){
        UserFactory.logout();
        $scope.user = null;
    }

    function register(username, password){
        UserFactory.register(username, password).then(function success(response){
            $scope.user = response.data.user;
        }, handleError);
    }

    function handleError(response){
        $scope.user_error += response.data;
    }
    // ======================================================================

    $scope.addCategory = '';
    $scope.catId = '';
    $scope.categoryList = function(id, name){//get list of categories and items
        $scope.detailItem='';
        $scope.items=[];
        if(id){
            $scope.catId = id;
            $scope.catName = name;
            var request = {
                method: 'GET',
                url: API_URL + '/itemlist/' + $scope.catId
            };
            var rez = $http(request);
            rez.success(function(data){
                $scope.items = data;
            });
            rez.error(function(data){
                alert(error + data);
            });
        }
        else{
            $scope.catId = '';
            $scope.catName='Root';
        }
        var request = {
            method: 'GET',
            url: API_URL + '/categorylist/' + $scope.catId
        };
        var rez = $http(request);
        rez.success(function(data){
            $scope.categories = data;
        });
        rez.error(function(data){
            alert(error + data);
        });


    };
    $scope.itemDetail = function(id){// get detail info about item from server
        var request = {
            method: 'GET',
            url: API_URL + '/itemdetail/' + id
        };
        var rez = $http(request);
        rez.success(function(data){
            $scope.detailItem = data;
        });
        rez.error(function(data){
            alert(error + data);
        });
    };
    $scope.categoryList();

});
})();