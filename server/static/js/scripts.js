(function(){
    'use strict';
    var app = angular.module('myApp', ['factories', 'ng.django.urls'], function config($httpProvider){
        $httpProvider.interceptors.push('AuthInterceptor');
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    });
<<<<<<< HEAD
    app.constant('API_URL', 'http://127.0.0.1:8000');
    app.controller('myCtrl', function($scope, $http, UserFactory, CommentFactory, RateFactory, djangoUrl){
        'use strict';
=======
app.controller('myCtrl', function($scope, $http, UserFactory, API_URL){
    'use strict';
>>>>>>> master


        // user authorization block
        // ======================================================================
        $scope.login = login;
        $scope.logout = logout;
        $scope.register = register;
        $scope.serverError = '';

        // initialization
        UserFactory.verifyUser().then(function success(response){
            $scope.user = response.data.user;
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
            }, handleServerError);
        }

        function logout(){
            UserFactory.logout();
            $scope.user = null;
        }

        function register(username, password){
            UserFactory.register(username, password).then(function success(response){
                $scope.user = response.data.user;
            }, handleServerError);
        }

        function handleServerError(response){
            $scope.serverError = response.status + " " + response.statusText;
            alert($scope.serverError);
        }
        // ======================================================================

        /*
        Comments and rates block
         */
        // ======================================================================
        $scope.setComment = setComment;
        $scope.setRate = setRate;

        $scope.setCommentError = null;
        $scope.setRateError = null;

        function setComment(commentInput){
            if (!$scope.user){
                $scope.setCommentError = "You need to sign in to leave a comment.";
                alert($scope.setCommentError);
            }
            else{
                CommentFactory.setComment(commentInput, $scope.detailItem.id, $scope.user.id, $scope.user.username)
                    .then(function success(response){
                    $scope.commentInput = '';
                    $scope.detailItem.comments_total = response.data.comments_total;
                    $scope.items.forEach(function(item) {
                      if (item.id == $scope.detailItem.id){
                          item.comments_total = $scope.detailItem.comments_total;
                      }

                    });
                }, handleServerError);
            }
        }

        function setRate(rateInput){
            if (!$scope.user){
                $scope.setRateError = "You need to sign in to set rate.";
                alert($scope.setRateError);
            }
            else{
                RateFactory.setRate(rateInput, $scope.detailItem.id, $scope.user.id).then(function success(response){
                    $scope.rateInput = null;
                    $scope.detailItem.average_rate = parseFloat(response.data.average_rate).toFixed(1);
                    $scope.items.forEach(function(item) {
                      if (item.id == $scope.detailItem.id){
                          item.average_rate = $scope.detailItem.average_rate;
                      }
                    });
                }, function error(response){
                    var error = response.data.non_field_errors;
                    alert(error);
                });
            }
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
                    url: djangoUrl.reverse('catalogue:item_list', [$scope.catId])
                };
                var rez = $http(request);
                //var rez = $http.get(API_URL + '/itemlist/' + $scope.catId);
                rez.success(function(data){
                    $scope.items = data;
                    $scope.items.forEach(function(item) {
                        item.average_rate = parseFloat(item.average_rate).toFixed(1);
                    });
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
            });
            rez.error(function(data){
                alert(error + data);
            });


        };
        $scope.itemDetail = function(id){// get detail info about item from server
            $scope.commentInput = $scope.rateInput = null; // clear form values when switching items
            var request = {
                method: 'GET',
                url: djangoUrl.reverse('catalogue:item_detail', [id])
            };
            var rez = $http(request);
            rez.success(function(data){
                $scope.detailItem = data;
                $scope.detailItem.average_rate = parseFloat($scope.detailItem.average_rate).toFixed(1);
            });
            rez.error(function(data){
                alert(error + data);
            });
        };
        $scope.categoryList();
    });
})();
