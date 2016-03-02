(function(){
    'use strict';
    var app = angular.module('factories', ['angular-jwt']);

    function successCallbackHandler(response){
            return response;
        }

    app.factory('UserFactory', function UserFactory($http, $q, AuthTokenFactory, djangoUrl){
        'use strict';
        return {
            login: login,
            logout: logout,
            verifyUser: verifyUser,
            refreshToken: refreshToken,
            register: register
        };

        function authSuccessCallbackHandler(response){
            AuthTokenFactory.setToken(response.data.token);
            return response;
        }

        function login(username, password){
            var url = djangoUrl.reverse('auth:login');
            return $http.post(url, {username: username, password: password})
                .then(authSuccessCallbackHandler)
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
                .then(successCallbackHandler)
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
                .then(successCallbackHandler)
        }

        function checkRateAlreadySet(userId, itemId){
            var url = djangoUrl.reverse('catalogue:check_rate_set', [userId, itemId]);
            return $http.get(url)
                .then(successCallbackHandler)
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
                .then(successCallbackHandler)
        }

        function getStore(storeId){
            var url = djangoUrl.reverse('stores:account_store', [storeId]);
            return $http.get(url)
                .then(successCallbackHandler)
        }
    });

    app.factory('CategoriesFactory', function CategoriesFactory($http, djangoUrl) {
        'use strict';
        return {
            getCategories: getCategories
        };

        function getCategories(){
            var url = djangoUrl.reverse('catalogue:categories_list');
            return $http.get(url)
                .then(successCallbackHandler)
        }
    });

    app.factory('ItemsFactory', function ItemsFactory($http, djangoUrl, $location) {
        'use strict';
        return {
            getItemsList: getItemsList,
            getItemDetails: getItemDetails,
            deleteItem: deleteItem,
            editItem: editItem,
            createItem: createItem
        };

        function getItemsList(category, store){
            var url = "";
            if (store.id === "master"){
                url = djangoUrl.reverse('catalogue:item_list', [category.cat_id]);
            }
            else{
                url = djangoUrl.reverse('stores:item_list', [category.cat_id, store.id])
            }

            return $http.get(url)
                .then(successCallbackHandler)
        }

        function getItemDetails(item){
            var itemId = null;
            if (item.id){
                itemId = item.id;
            }
            else{
                itemId = item.item_id;
            }
            var url = djangoUrl.reverse('catalogue:item_detail', [itemId]);
            return $http.get(url)
                .then($location.path(url), successCallbackHandler)
        }

        function deleteItem(itemId){
            var url = djangoUrl.reverse('stores:update_delete_item', [itemId]);
            return $http.delete(url)
                .then(successCallbackHandler)
        }

        function editItem(item){
            var itemId = null;
            if (item.id){
                itemId = item.id;
            }
            else{
                itemId = item.item_id;
            }
            var url = djangoUrl.reverse('stores:update_delete_item', [itemId]);
            var data = {
                name: item.name,
                price: item.price,
                category: item.category,
                description: item.description,
                //image_url: item.image_url,
                store: item.store,
                quantity: item.quantity,
                running_out_level: item.running_out_level
            };
            return $http.put(url, data)
                .then(successCallbackHandler)
        }

        function createItem(item){
            var url = djangoUrl.reverse('stores:add_item');
            var data = {
                name: item.name,
                price: item.price,
                category: item.category,
                description: item.description,
                //image_url: "",
                store: item.store,
                quantity: item.quantity,
                running_out_level: item.running_out_level
            };
            return $http.post(url, data)
                .then(successCallbackHandler)
        }
    });

    app.factory('CartFactory', function CartFactory($http, djangoUrl) {
        'use strict';
        return {
            purchase: purchase
        };

        function purchase(data){
            var url = djangoUrl.reverse('cart:add_item_in_cart');
            return $http.post(url, data)
                .then(successCallbackHandler)
        }
    });

})();
