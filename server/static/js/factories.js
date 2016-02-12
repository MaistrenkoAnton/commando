(function(){
    'use strict';
var app = angular.module('authentication', []);

    app.factory('UserFactory', function UserFactory($http, $q, API_URL, AuthTokenFactory){
        'use strict';
        return {
            login: login,
            logout: logout,
            verifyUser: verifyUser,
            register: register
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

        function register(username, password){
            return $http.post(API_URL + '/auth/api-registration/', {username: username, password: password})
                .then(function success(response){
                    AuthTokenFactory.setToken(response.data.token);
                    return response;
                })
        }

        function verifyUser(){
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