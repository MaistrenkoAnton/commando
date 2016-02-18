(function(){
    'use strict';
    var app = angular.module('factories', ['angular-jwt']);

    app.factory('UserFactory', function UserFactory($http, $q, AuthTokenFactory, djangoUrl){
        'use strict';
        return {
            login: login,
            logout: logout,
            verifyUser: verifyUser,
            refreshToken: refreshToken,
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
                    return response;
                })
        }

        function refreshToken(){
            var token = AuthTokenFactory.getToken();
            if (token){
                var url = djangoUrl.reverse('auth:refresh');
                return $http.post(url, {token: token});
            }
            else{
                return $q.reject({data: 'No token in local storage'});
            }
        }


        function verifyUser(){
            var token = AuthTokenFactory.getToken();
            if (token){
                var url = djangoUrl.reverse('auth:verify');
                return $http.post(url, {token: token});
            }
            else{
                return $q.reject({data: 'No token in local storage'});
            }
        }
    });

    app.factory('AuthTokenFactory', function AuthTokenFactory($window, jwtHelper){
        'use strict';
        var store = $window.localStorage;
        var key = 'auth-token';
        return {
            getToken: getToken,
            setToken: setToken
        };

        function getToken(){
            if (store.getItem(key) && jwtHelper.isTokenExpired(store.getItem(key))){
                store.removeItem(key);
            }
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
                config.headers.Authorization = 'JWT ' + token;
            }
            return config;
        }
    });

    app.factory('CommentFactory', function CommentFactory($http, AuthTokenFactory, djangoUrl){
        'use strict';
        return {
            setComment: setComment
        };

        function setComment(commentInput, itemId, userId, username){
            var url = djangoUrl.reverse('catalogue:add_comment');
            var data = {text: commentInput,
                        item: itemId,
                        user: userId,
                        author: username};
            return $http.post(url, data)
                .then(function success(response){
                    return response;
                })
        }
    });

    app.factory('RateFactory', function RateFactory($http, AuthTokenFactory, djangoUrl){
        'use strict';
        return {
            setRate: setRate
        };

        function setRate(rateInput, itemId, userId){
            var url = djangoUrl.reverse('catalogue:set_rate');
            var data = {rate: rateInput,
                        item: itemId,
                        user: userId};
            return $http.post(url, data)
                .then(function success(response){
                    return response;
                })
        }
    });

})();
