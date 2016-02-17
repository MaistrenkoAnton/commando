(function(){
    'use strict';
    var app = angular.module('myApp', ['authentication', 'ng.django.urls'], function config($httpProvider){
        $httpProvider.interceptors.push('AuthInterceptor');
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    });
    app.constant('API_URL', 'http://127.0.0.1:8000');
    app.controller('myCtrl', function($scope, $http, UserFactory, djangoUrl){
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
            console.log(username + "  " + password);
            UserFactory.register(username, password).then(function success(response){
                $scope.user = response.data.user;
            }, handleError);
        }

        function handleError(response){
            $scope.user_error += response.data;
            alert($scope.user_error);
        }
        // ======================================================================

        $scope.addCategory = '';
        $scope.catId = '';
        $scope.categoryList = function(id, name){//get list of categories and items
            $scope.detailItem='';
            $scope.items=[];
            if(id){
                console.log('id = ' + id);
                $scope.catId = id;
                $scope.catName = name;
                var request = {
                    method: 'GET',
                    url: djangoUrl.reverse('catalogue:item_list', [$scope.catId])
                };
                var rez = $http(request);
                //var rez = $http.get(API_URL + '/itemlist/' + $scope.catId);
                rez.success(function(data){
                    console.log(data)
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
            if ($scope.catId == '') {
                var request = {
                    method: 'GET',
                    url: djangoUrl.reverse('catalogue:category_list_root')
                };
            } else{
                var request = {
                    method: 'GET',
                    url: djangoUrl.reverse('catalogue:category_list', [$scope.catId])
                };
            }
            var rez = $http(request);
            rez.success(function(data){
                $scope.categories = data;
                console.log(data);
            });
            rez.error(function(data){
                alert(error + data);
            });


        };
        $scope.itemDetail = function(id){// get detail info about item from server
            var request = {
                method: 'GET',
                url: djangoUrl.reverse('catalogue:item_detail', [id])
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
