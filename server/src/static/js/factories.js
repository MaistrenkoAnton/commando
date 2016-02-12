(function(){
    'use strict';
    var app = angular.module('authentication', []);

    app.factory('UserFactory', function UserFactory($http, $q, AuthTokenFactory, djangoUrl){
        'use strict';
        return {
            login: login,
            logout: logout,
            verifyUser: verifyUser,
            register: register
        };

        function login(username, password){
            var url = djangoUrl.reverse('auth:login');
            return $http.post(url, {username: username, password: password})
                .then(function success(response){
                    AuthTokenFactory.setToken(response.data.token);
                    return response;
                })
        }

        function logout(){
            AuthTokenFactory.setToken();
        }

        function register(username, password){
            var url = djangoUrl.reverse('auth:register');
            return $http.post(url, {username: username, password: password})
                .then(function success(response){
                    AuthTokenFactory.setToken(response.data.token);
                    console.log(response);
                    return response;
                })
        }

        function verifyUser(){
            var token = AuthTokenFactory.getToken();
            if (token){
                var url = djangoUrl.reverse('auth:verify');
                return $http.post(url, {token: token});
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