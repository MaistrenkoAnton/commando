/**
 * Created by user on 10.02.16.
 */
(function(){
    'use strict';
    var app = angular.module('app', [], function config($httpProvider){
        $httpProvider.interceptors.push('AuthInterceptor');
    });
    app.constant('API_URL', 'http://127.0.0.1:8000');
    //app.config(['$httpProvider', function($httpProvider) {
    //    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    //    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    //    //$httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    //    $httpProvider.defaults.headers.post['Content-Type'] = 'application/json';
    //}]);
    app.controller('MainCtrl', function MainCtrl(RandomUserFactory, UserFactory){
        'use strict';
        var vm = this;
        vm.getRandomUser = getRandomUser;
        vm.login = login;
        vm.logout = logout;

        // initialization
        UserFactory.getUser().then(function success(response){
            vm.user = response.data;
        });

       function getRandomUser() {
           RandomUserFactory.getUser().then(function success(response) {
               vm.randomUser = response.data;
               console.log(vm.randomUser);
           }, handleError);
       }
        function login(username, password){
            UserFactory.login(username, password).then(function success(response){
                vm.user = response.data.user;
            }, handleError);
        }

        function logout(){
            UserFactory.logout();
            vm.user = null;
        }

        function handleError(response){
            alert('Error! ' + response.data)
        }
    });

    app.factory('RandomUserFactory', function RandomUserFactory($http, API_URL){
        'use strict';
        return {
            getUser: getUser
        };

        function getUser(){
            return $http.get(API_URL + '/auth/api-get-user/1/')
        }
    });

    app.factory('UserFactory', function UserFactory($http, $q, API_URL, AuthTokenFactory){
        'use strict';
        return {
            login: login,
            logout: logout,
            getUser: getUser
        };

        function login(username, password){
            return $http.post(API_URL + '/auth/api-token-auth/', {username: username, password: password})
                .then(function success(response){
                    AuthTokenFactory.setToken(response.data.token);
                    return response;
                })
        }

        function logout(){
            AuthTokenFactory.setToken();
        }

        function getUser(){
            var token = AuthTokenFactory.getToken();
            if (token){
                return $http.post(API_URL + '/auth/api-token-verify/', {token: token});
            }
            else{
                return $q.reject({data: 'Client has no auth token'});
            }
        }
    });


    app.factory('AuthTokenFactory', function AuthTokenFactory($window){
        'use strict';
        var store = $window.localStorage;
        var key = 'auth-token';
        return {
            getToken: getToken,
            setToken: setToken
        };

        function getToken(){
            return store.getItem(key);
        }

        function setToken(token){
            if (token){
                store.setItem(key, token);
            }
            else{
               store.removeItem(key);
            }
        }
    });

    app.factory('AuthInterceptor', function AuthInterceptor(AuthTokenFactory){
        'use strict';
        return {
            request: addToken
        };

        function addToken(config){
            var token = AuthTokenFactory.getToken();
            if (token){
                config.headers = config.headers || {};
                config.headers.Authorization = 'Bearer ' + token;
            }
            return config;
        }
    });
})();