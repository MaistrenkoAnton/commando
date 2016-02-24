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
            setRate: setRate,
            checkRateAlreadySet: checkRateAlreadySet
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

        function checkRateAlreadySet(userId, itemId){
            var url = djangoUrl.reverse('catalogue:check_rate_set', [userId, itemId]);
            return $http.get(url)
                .then(function success(response){
                    return response;
                })
        }
    });

    app.factory('StoresFactory', function StoresFactory($http, djangoUrl){
        'use strict';
        return {
            getStoresList: getStoresList,
            getStore: getStore
        };

        function getStoresList(){
            var url = djangoUrl.reverse('stores:store_list');
            return $http.get(url)
                .then(function success(response){
                    return response;
                })
        }

        function getStore(storeId){
            var url = djangoUrl.reverse('stores:account_store', [storeId]);
            return $http.get(url)
                .then(function success(response){
                    return response;
                })
        }
    });

    app.factory('CategoriesFactory', function CategoriesFactory($http, djangoUrl) {
        'use strict';
        return {
            getCategoriesList: getCategoriesList
        };

        function getCategoriesList(parentCategory){
            var url = '';
            if (parentCategory){
                url = djangoUrl.reverse('catalogue:category_list', [parentCategory.id])
            }
            else {
                url = djangoUrl.reverse('catalogue:category_list_root')
            }
            return $http.get(url)
                .then(function success(response){
                    return response;
                })
        }
    });

    app.factory('ItemsFactory', function ItemsFactory($http, djangoUrl) {
        'use strict';
        return {
            getItemsList: getItemsList,
            getItemDetails: getItemDetails
        };

        function getItemsList(category, store){
            var url = "";
            if (store.id == "master"){
                url = djangoUrl.reverse('catalogue:item_list', [category.id]);
            }
            else{
                url = djangoUrl.reverse('stores:item_list', [category.id, store.id])
            }
            return $http.get(url)
                .then(function success(response){
                    return response;
                })
        }

        function getItemDetails(item){
            var url = djangoUrl.reverse('catalogue:item_detail', [item.id]);
            return $http.get(url)
                .then(function success(response){
                    return response;
                })
        }
    });

})();
