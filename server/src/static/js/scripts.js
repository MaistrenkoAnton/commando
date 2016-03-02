(function(){
    'use strict';
    var app = angular.module('myApp', ['factories', 'ng.django.urls'], function config($httpProvider, $locationProvider){
        $httpProvider.interceptors.push('AuthInterceptor');
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $locationProvider.html5Mode({enabled: true, requireBase: false}).hashPrefix('!');
    });
    app.controller('myCtrl', function($scope, $http, UserFactory, CommentFactory, RateFactory, StoresFactory,
                                      CategoriesFactory, ItemsFactory, CartFactory){
        'use strict';




        // user authorization block
        // ======================================================================
        $scope.login = login;
        $scope.logout = logout;
        $scope.register = register;
        $scope.toggleAuthForm = toggleAuthForm;
        $scope.hideAuthForms = hideAuthForms;
        $scope.serverError = '';
        $scope.showModalLogin = false;
        $scope.showModalRegister = false;

        $scope.userIsAuthenticated = userIsAuthenticated;
        $scope.userIsStaff = userIsStaff;

        // initialization
        UserFactory.verifyUser().then(function success(response){
            $scope.user = response.data.user;
            $scope.user.canSetRate = true;
        });

        function hideAuthForms(){
            $scope.showModalLogin = false;
            $scope.showModalRegister = false;
        }

        function userIsAuthenticated(){
            return $scope.user ? true: false;
        }

        function userIsStaff(){
            return ($scope.user && $scope.user.is_staff === true) ? true: false;
        }

        $scope.signInForm = true;
        $scope.signUpForm = false;
        $scope.sign_link = 'Sign Up';
        $scope.setForm = setForm;

        function toggleAuthForm(formType){

            switch (formType){
                case 'login':
                    $scope.showModalLogin = !$scope.showModalLogin;
                    break;
                case 'register':
                    $scope.showModalRegister = !$scope.showModalRegister;
                    break;
            }
        }

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
                if ($scope.currentItem){
                    $scope.user.canSetRate = checkRateAlreadySet($scope.user.id, $scope.currentItem.id);
                }
                $scope.user.canSetRate = true;
                if ($scope.cart){
                    $scope.cart = null;
                }
            }, handleServerError);

        }

        function logout(){
            UserFactory.logout();
            $scope.user = null;
            $scope.cart = null;
        }

        function register(username, password){
            UserFactory.register(username, password).then(function success(response){
                $scope.user = response.data.user;
                if ($scope.currentItem){
                    $scope.user.canSetRate = checkRateAlreadySet($scope.user.id, $scope.currentItem.id);
                }
                $scope.user.canSetRate = true;
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

        $scope.alreadySetRate = false;
        $scope.checkRateAlreadySet = checkRateAlreadySet;
        $scope.setRate = setRate;
        $scope.setComment = setComment;

        function checkRateAlreadySet(userId, itemId){
            RateFactory.checkRateAlreadySet(userId, itemId).then(function success(response){
                return Boolean(response.data);
            }, handleServerError);
        }

        function setRate(rateInput){
            if (!$scope.user){
                alert("You need to be logged in to set rate.");
            }
            else if (!$scope.user.canSetRate){
                alert("You've already set rate to this item");
            }
            else{
                RateFactory.setRate(rateInput, $scope.currentItem.id, $scope.user.id)
                    .then(function success(response){
                        $scope.currentItem.average_rate = response.data.average_rate;
                        $scope.currentItem.stars = generateStarsArray($scope.currentItem.average_rate);
                        $scope.user.canSetRate = false;
                        $scope.rateInput = null;
                    }, handleServerError);
            }
        }

        function setComment(commentInput){
            if (!$scope.user){
                alert("You need to be logged in to leave the comment.");
            }
            else{
                CommentFactory.setComment(commentInput, $scope.currentItem.id, $scope.user.id, $scope.user.username)
                    .then(function success(response){
                        $scope.currentItem.comments_total = response.data.comments_total;
                        $scope.commentInput = null;
                    }, handleServerError);
            }
        }

        // CATEGORIES AND ITEMS BLOCK
        // =================================================================================================

        $scope.itemsList = [];
        $scope.categoriesList = [];
        $scope.currentCategory = null;
        $scope.currentItem = null;
        $scope.detailItem = null;
        $scope.isCurrentItem = null;
        $scope.itemsFieldState = null;

        $scope.isCurrentItem = isCurrentItem;
        $scope.setCurrentCategory = setCurrentCategory;
        $scope.noItems = noItems;
        $scope.setCurrentItem = setCurrentItem;
        $scope.resetItemData = resetItemData;
        $scope.getCategories = getCategories;
        $scope.getItemsList = getItemsList;
        $scope.getItemDetails = getItemDetails;

        function isCurrentItem(item) {
            return $scope.currentItem && item.name === $scope.currentItem.name;
        }

        function noItems(){
            return $scope.itemsList.length > 0;
        }

        function setCurrentItem(item){
            $scope.getItemDetails(item);
            $scope.itemsFieldState = "itemDetails";
        }

        function setCurrentCategory(category) {
            $scope.currentCategory = category;
            $scope.resetItemData();
            $scope.getCategories();
            $scope.getItemsList(category);
            $scope.itemsFieldState = 'itemsList';
        }

        function getCategories(){
            CategoriesFactory.getCategories().then(function success(response){
                if (response.data.data.length > 0){
                    $scope.categoriesList = response.data.data;
                    $scope.canShowActiveCategory = false;
                }
                else {
                    $scope.canShowActiveCategory = true;
                }
                if (response.data.facet.fields.parent){
                    response.data.facet.fields.parent.forEach(
                        function(item)
                        {
                            for (var i = 0; i < $scope.categoriesList.length; i++){
                                if ($scope.categoriesList[i].cat_id === parseInt(item[0])){
                                    $scope.categoriesList[i].facet = item[1];
                                }
                            }
                        }
                    );
                }
            }, handleServerError);
        }

        function generateStarsArray(rate){
            var starsArray = [];
            var fullStars = Math.floor(rate);
            var delta = rate - fullStars;
            if (delta > 0.8){
                fullStars ++;
                delta = null;
            }
            else if(delta < 0.4){
                delta = null;
            }
            for (var i = 0; i < 5; i++){
                if (fullStars >= i+1){
                    starsArray.push("full");
                }
                else if( ((i === 0) || (starsArray[i-1] === "full")) && delta){
                    starsArray.push("half");
                }
                else{
                    starsArray.push("empty");
                }
            }
            return starsArray;
        }

        function toFixed(value, precision) {
            var precision = precision || 0,
                power = Math.pow(10, precision),
                absValue = Math.abs(Math.round(value * power)),
                result = (value < 0 ? '-' : '') + String(Math.floor(absValue / power));

            if (precision > 0) {
                var fraction = String(absValue % power),
                    padding = new Array(Math.max(precision - fraction.length, 0) + 1).join('0');
                result += '.' + padding + fraction;
            }
            return result;
        }

        function getItemsList(category){
            ItemsFactory.getItemsList(category, $scope.currentStore).then(function success(response){
                $scope.itemsList = response.data.data;
                if ($scope.itemsList && $scope.itemsList.length > 0){
                    $scope.itemsFieldState = "itemsList";
                }
                if ($scope.itemsList){
                    for (var i = 0; i < $scope.itemsList.length; i++){
                        if ($scope.itemsList[i].discount > 0){
                            var newPrice = $scope.itemsList[i].price * (100 - $scope.itemsList[i].discount) / 100;
                            $scope.itemsList[i].newPrice = toFixed(newPrice, 2);
                        }
                        $scope.itemsList[i].stars = generateStarsArray($scope.itemsList[i].average_rate)
                    }
                }
            })
        }

        function getItemDetails(item){
            ItemsFactory.getItemDetails(item).then(function success(response){
                $scope.currentItem = response.data;
                if ($scope.currentItem.stock.discount){
                    var newPrice = $scope.currentItem.price * (100 - $scope.currentItem.stock.discount) / 100;
                    $scope.currentItem.newPrice = toFixed(newPrice, 2);
                }
                $scope.currentItem.stars = generateStarsArray($scope.currentItem.average_rate);
                $scope.rateInput = null;
                if ($scope.user){
                    $scope.user.canSetRate = !checkRateAlreadySet($scope.user.id, $scope.currentItem.id);
                }
            })
        }

        // initialize categories and items data on start
        getCategories();

        function resetItemData(){
            $scope.itemsList = [];
            $scope.currentItem = null;
            $scope.isCurrentItem = null;
            if ($scope.user){
                $scope.user.canSetRate = false;
            }
            $scope.rateInput = null;
            $scope.cancelCreatingItem();
            $scope.cancelEditingItem();
            if ($scope.newItem) {$scope.newItem = null;}
        }

        // ITEMS CRUD BLOCK
        // =================================================================================================

        // Edit
        $scope.editedItem = null;
        $scope.isEditingItem = false;
        $scope.startEditingItem = startEditingItem;
        $scope.cancelEditingItem = cancelEditingItem;
        $scope.setEditedItem = setEditedItem;
        $scope.editItem = editItem;

        function editItem(item){
            if (typeof item.category === 'object'){
                item.category = item.category.cat_id;
            }
            ItemsFactory.editItem(item).then(function success(response){
                $scope.setCurrentItem(response.data);
                $scope.isEditingItem = false;
                $scope.editedItem = null;
            });
        }

        function setEditedItem(item) {
            $scope.editedItem = angular.copy(item);
        }

        function startEditingItem(item) {
            if (!$scope.userIsStaff()){
                alert("You need to be logged in as staff member to edit items!");
            }
            else if (!$scope.currentStore || $scope.currentStore.id != item.store){
                alert("This item is not from this store!");
            }
            else{
                $scope.itemsFieldState = "itemEdit";
                $scope.setEditedItem(item);
                $scope.setAllCategories(item);
                $scope.isEditingItem = true;
            }
        }

        function cancelEditingItem(){
            $scope.editedItem = null;
            $scope.isEditingItem = false;
            $scope.allCategories = null;
        }

        // Create
        $scope.isCreatingItem = false;
        $scope.createItem = createItem;
        $scope.resetCreateItemForm = resetCreateItemForm;
        $scope.cancelCreatingItem = cancelCreatingItem;
        $scope.startCreatingItem = startCreatingItem;

        function startCreatingItem() {
            if (!$scope.userIsStaff()){
                alert("You need to be logged in as staff member to edit items!");
            }
            else if ($scope.currentStore.id === 'master'){
                alert("You can not create items from Master store!");
            }
            else{
                $scope.itemsFieldState = "itemCreate";
                $scope.createdItem = {
                    name: '',
                    price: null,
                    category: null,
                    description: '',
                    store: $scope.currentStore.id,
                    quantity: null,
                    running_out_level: null
                };
                $scope.isCreatingItem = true;
                $scope.setAllCategories();
            }
        }

        function cancelCreatingItem(){
            $scope.createdItem = null;
            $scope.allCategories = null;
            $scope.isCreatingItem = false;

        }

        function resetCreateItemForm(){
            $scope.createdItem = {
                name: '',
                price: null,
                category: null,
                description: '',
                store: $scope.currentStore.id,
                quantity: null,
                running_out_level: null
            };
        }

        function createItem(item){
            ItemsFactory.createItem(item).then(function success(response){
                $scope.setCurrentItem(response.data);
                $scope.cancelCreatingItem();
            }, handleServerError);
        }

        // Delete
        $scope.deleteItem = deleteItem;

        function deleteItem(item){
            if ($scope.userIsStaff()){
                var itemId = null;
                if (item.id){
                    itemId = item.id;
                }
                else{
                    itemId = item.item_id;
                }
                ItemsFactory.deleteItem(itemId).then(function success(response){
                    $scope.setCurrentCategory($scope.currentCategory);
                })
            }
            else{
                alert("You need to be logged in as staff member to delete items!");
            }
        }

        // utility
        $scope.setAllCategories = setAllCategories;
        $scope.showCreateItemButton = showCreateItemButton;
        $scope.showEditDeleteItemButtons = showEditDeleteItemButtons;

        function showEditDeleteItemButtons(){
            return $scope.currentStore.id != 'master' && $scope.userIsStaff();
        }

        function showCreateItemButton(){
            return $scope.currentStore.id != 'master' && $scope.userIsStaff() && !$scope.createdItem && !$scope.editedItem;
        }

        function setAllCategories(item){
            CategoriesFactory.getCategories().then(function success(response){
                $scope.allCategories = {
                    availableOptions: response.data.data
                };
                if (item){
                    for (var i = 0; i < $scope.allCategories.availableOptions.length; i++){
                        if (item.category === $scope.allCategories.availableOptions[i].cat_id ||
                            item.category.cat_id === $scope.allCategories.availableOptions[i].cat_id){
                            $scope.editedItem.category = $scope.allCategories.availableOptions[i];
                        }
                    }
                }
                else{
                    $scope.createItem.selectedOption = null;
                }
            }, handleServerError);
        }
        // =================================================================================================

        // STORES
        // ===============================
        $scope.getStore = getStore;
        $scope.setCurrentStore = setCurrentStore;
        $scope.setMasterStore = setMasterStore;
        $scope.getStoresList = getStoresList;

        function setMasterStore(){
            $scope.currentStore = {
                title: "MasterStore",
                id: "master"
            }
        }

        function getStoresList(){
            StoresFactory.getStoresList().then(function success(response){
                $scope.stores = [$scope.currentStore];
                $scope.stores = $scope.stores.concat(response.data);
            }, handleServerError);
        }

        // initialize stores
        setMasterStore();
        getStoresList();

        function getStore(storeId){
            StoresFactory.getStore(storeId).then(function success(response){
                $scope.currentStore = response.data;
            })
        }

        function setCurrentStore(store){
            $scope.cancelCreatingItem();
            $scope.cancelEditingItem();
            $scope.currentStore = store;
        }

        // CART
        // =======================================================================
        $scope.cart = null;
        $scope.addToCart = addToCart;
        $scope.showCart = showCart;
        $scope.canShowCartButton = canShowCartButton;
        $scope.removeFromCart = removeFromCart;
        $scope.purchase = purchase;

        function canShowCartButton(){
            return $scope.user && $scope.currentStore.id != 'master' && $scope.itemsFieldState != 'cart';
        }

        function addToCart(item){
            var itemId = (item.id ? item.id : item.item_id);
            var itemAdded = false;
            if (!$scope.user){
                alert("You need to be logged in to add items to cart!");
            }
            else if (!$scope.cart){
                $scope.cart = {
                    user: $scope.user.id,
                    items: [
                        {
                            checked: true,
                            name: item.name,
                            id: itemId,
                            quantity: 1
                        }
                    ]
                };
            }
            else{
                for (var i = 0; i < $scope.cart.items.length; i++){
                    if (itemId === $scope.cart.items[i].id){
                        $scope.cart.items[i].quantity ++;
                        itemAdded = true;
                        break;
                    }
                }
                if (!itemAdded){
                    $scope.cart.items.push({
                        checked: true,
                        name: item.name,
                        id: itemId,
                        quantity: 1
                    });
                }
            }
        }

        function removeFromCart(item, cart){
            var itemIndex = $scope.cart.items.indexOf(item);
            cart.items.splice(itemIndex, 1);
        }

        function showCart(){
            $scope.stateBeforeCart = $scope.itemsFieldState;
            $scope.itemsFieldState = 'cart'
        }

        function purchase(cart){
            var itemsToRemove = [];
            for (var i = 0; i < cart.items.length; i++){
                if (cart.items[i].checked != true || cart.items[i].quantity === 0){
                    itemsToRemove.push($scope.cart.items[i])
                }
                else{
                    delete cart.items[i].checked;
                    delete cart.items[i].name;
                }
            }
            for (i = 0; i < itemsToRemove.length; i++){
                $scope.removeFromCart(itemsToRemove[i], cart);
            }
            CartFactory.purchase(cart).then(function success(response){
                alert("Purchase sucessful!");
                $scope.cart = null;
                $scope.itemsFieldState = $scope.stateBeforeCart;
                $scope.stateBeforeCart = null;
            })
        }

        // =======================================================================

    });

    app.directive('modal', function () {
        return {
            template: '<div class="modal fade">' +
            '<div class="modal-dialog">' +
            '<div class="modal-content">' +
            '<div class="modal-header">' +
            '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>' +
            '<h4 class="modal-title">{{ title }}</h4>' +
            '</div>' +
            '<div class="modal-body" ng-transclude></div>' +
            '</div>' +
            '</div>' +
            '</div>',
            restrict: 'E',
            transclude: true,
            replace:true,
            scope:true,
            link: function postLink(scope, element, attrs) {
                scope.title = attrs.title;

                scope.$watch(attrs.visible, function(value){
                    if(value == true)
                        $(element).modal('show');
                    else
                        $(element).modal('hide');
                });

                $(element).on('shown.bs.modal', function(){
                    scope.$apply(function(){
                        scope.$parent[attrs.visible] = true;
                    });
                });

                $(element).on('hidden.bs.modal', function(){
                    scope.$apply(function(){
                        scope.$parent[attrs.visible] = false;
                    });
                });
            }
        };
    });
})();
