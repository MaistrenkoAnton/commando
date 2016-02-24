(function(){
    'use strict';
    var app = angular.module('myApp', ['factories', 'ng.django.urls'], function config($httpProvider){
        $httpProvider.interceptors.push('AuthInterceptor');
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    });
    app.constant('API_URL', 'http://127.0.0.1:8000');
    app.controller('myCtrl', function($scope, $http, UserFactory, CommentFactory, RateFactory, StoresFactory,
                                      CategoriesFactory, ItemsFactory, djangoUrl){
        'use strict';

        // user authorization block
        // ======================================================================
        $scope.login = login;
        $scope.logout = logout;
        $scope.register = register;
        $scope.serverError = '';

        $scope.userIsAuthenticated = userIsAuthenticated;
        $scope.userIsStaff = userIsStaff;

        // initialization
        UserFactory.verifyUser().then(function success(response){
            $scope.user = response.data.user;
            $scope.user.canSetRate = true;
        });

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
            }, handleServerError);
        }

        function logout(){
            UserFactory.logout();
            $scope.user = null;
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

        function canSetRate(){
            if (!$scope.user){
                return [false, "You need to be logged in to set rate."]
            }
            else{
                checkRateAlreadySet();
                if ($scope.alreadySetRate){
                    return [false, "You've already set rate to this item"];
                }
                else{
                    return [true];
                }
            }
        }

        function checkRateAlreadySet(userId, itemId){
            RateFactory.checkRateAlreadySet(userId, itemId).then(function success(response){
                return Boolean(response.data);
            }, handleServerError);
        }

        $scope.setRate = setRate;

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

        $scope.setComment = setComment;

        function setComment(commentInput){
            if (!$scope.user){
                alert("You need to be logged in to leave the comment.");
            }
            else{
                CommentFactory.setComment(commentInput, $scope.currentItem.id, $scope.user.id, $scope.user.username)
                    .then(function success(response){
                        $scope.currentItem.comments_total = response.data.comments_total;
                        for (var i = 0; i < $scope.itemsList.length; i++){
                            if ($scope.itemsList[i].id == $scope.currentItem.id){
                                $scope.itemsList[i].comments_total = $scope.currentItem.comments_total
                            }
                        }
                        $scope.commentInput = null;
                    }, handleServerError);
            }
        }

        // CATEGORIES AND ITEMS BLOCK
        // =================================================================================================

        // items and categories data initials
        $scope.itemsList = [];
        $scope.categoriesList = [];
        $scope.parentCategoriesList = [];
        $scope.currentCategory = null;
        $scope.currentItem = null;
        $scope.detailItem = null;


        // items ang categories states
        $scope.isCreatingItem = false;
        $scope.isEditingItem = false;
        $scope.isCurrentCategory = null;
        $scope.isCurrentItem = null;
        $scope.editedItem = null;


        $scope.isCurrentCategory = isCurrentCategory;
        $scope.isCurrentItem = isCurrentItem;
        $scope.setCurrentCategory = setCurrentCategory;
        $scope.setCategoryBack = setCategoryBack;

        $scope.noParentCategories = noParentCategories;
        $scope.canShowActiveCategory = false;
        $scope.parentCategoryActive = parentCategoryActive;
        $scope.noItems = noItems;
        $scope.setCurrentItem = setCurrentItem;

        function noParentCategories(){
            return $scope.parentCategoriesList.length == 0;
        }


        function parentCategoryActive(category){
            var res = $scope.parentCategoriesList.length > 0 && category == $scope.parentCategoriesList[-1];
            return res;
        }

        function isCurrentCategory(category) {
            return $scope.currentCategory && category.name === $scope.currentCategory.name && $scope.canShowActiveCategory == true;
        }

        function isCurrentItem(item) {
            return $scope.currentItem && item.name === $scope.currentItem.name;
        }

        function noItems(){
            return $scope.itemsList.length > 0;
        }

        function setCurrentItem(item){
            $scope.getItemDetails(item);
        }

        function setCurrentCategory(category) {
            if ($scope.canShowActiveCategory){
                $scope.parentCategoriesList.pop();
            }
            $scope.parentCategoriesList.push(category);
            $scope.currentCategory = category;
            $scope.resetItemData();
            $scope.getCategoriesList(category);
            $scope.getItemsList(category);
        }

        function setCategoryBack(category){
            if (category){
                var targetCategoryIndex = $scope.parentCategoriesList.indexOf(category);
                $scope.parentCategoriesList.splice(-targetCategoryIndex);
                $scope.setCurrentCategory(category)
            }
            else {
                $scope.resetCategoriesData();
            }
        }


        $scope.getCategoriesList = getCategoriesList;
        $scope.getItemsList = getItemsList;
        $scope.getItemDetails = getItemDetails;

        function getCategoriesList(category){
            CategoriesFactory.getCategoriesList(category).then(function success(response){
                if (response.data.data.length > 0){
                    $scope.categoriesList = response.data.data;
                    $scope.canShowActiveCategory = false;
                }
                else {
                    $scope.canShowActiveCategory = true;
                }
                response.data.facet.fields.parent.forEach(
                    function(item)
                    {
                        for (var i = 0; i < $scope.categoriesList.length; i++){
                            if ($scope.categoriesList[i].id == item[0]){
                                $scope.categoriesList[i].facet = item[1];
                            }
                        }
                    }
                );
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
                else if( ((i == 0) || (starsArray[i-1] == "full")) && delta){
                    starsArray.push("half");
                }
                else{
                    starsArray.push("empty");
                }
            }
            return starsArray;
        }

        function getItemsList(category){
            ItemsFactory.getItemsList(category, $scope.currentStore).then(function success(response){

                $scope.itemsList = response.data.data;
                if ($scope.itemsList){
                    for (var i = 0; i < $scope.itemsList.length; i++){
                        $scope.itemsList[i].stars = generateStarsArray($scope.itemsList[i].average_rate)
                    }
                }
                console.log(response);
            })
        }

        function getItemDetails(item){
            ItemsFactory.getItemDetails(item).then(function success(response){
                $scope.currentItem = response.data;
                $scope.currentItem.stars = generateStarsArray($scope.currentItem.average_rate);
                $scope.rateInput = null;
                if ($scope.user){
                    $scope.user.canSetRate = !checkRateAlreadySet($scope.user.id, $scope.currentItem.id);
                }
            })
        }

        // initialize categories and items data on start
        getCategoriesList();


        $scope.resetCategoriesData = resetCategoriesData;

        function resetCategoriesData(){
            $scope.categoriesList = [];
            $scope.parentCategoriesList = [];
            $scope.currentCategory = null;
            $scope.getCategoriesList();
            $scope.resetItemData();
        }


        $scope.resetItemData = resetItemData;

        function resetItemData(){
            $scope.itemsList = [];
            $scope.currentItem = null;
            $scope.isCurrentItem = null;
            if ($scope.user){
                $scope.user.canSetRate = false;
            }
            $scope.rateInput = null;
            cancelCreatingItem();
            cancelEditingItem();
            if ($scope.newItem) {$scope.newItem = null;}
        }


        function setEditedItem(item) {
            $scope.editedItem = angular.copy(item);
        }

        function isSelectedItem(item) {
            return $scope.editedItem !== null && $scope.editedItem.id === item.id;
        }

        $scope.setEditedBookmark = setEditedItem;
        $scope.isSelectedBookmark = isSelectedItem;

        function resetCreateItemForm() {
            $scope.newItem = {
                name: '',
                price: '',
                image_url: '',
                description: '',
                category: '',
                quantity: '',
                running_out_level: '',
                store: $scope.store.id
            };
        }

        function shouldShowCreatingItem() {
            return $scope.accountStoreActive && !$scope.isEditingItem && $scope.userIsStaff;
        }

        function startCreatingItem() {
            $scope.isCreatingItem = true;
            $scope.isEditingItem = false;
            resetCreateItemForm();
        }

        function cancelCreatingItem() {
            $scope.isCreating = false;
        }

        $scope.shouldShowCreatingItem = shouldShowCreatingItem;
        $scope.startCreatingItem = startCreatingItem;
        $scope.cancelCreatingItem = cancelCreatingItem;

        function shouldShowEditingItem() {
            return $scope.store && !$scope.isCreatingItem && $scope.userIsStaff;
        }

        function startEditingItem() {
            $scope.isCreatingItem = false;
            $scope.isEditingItem = true;
        }

        function cancelEditingItem() {
            $scope.isEditingItem = false;
            $scope.editedItem = null;
        }

        $scope.startEditingItem = startEditingItem;
        $scope.cancelEditingItem = cancelEditingItem;
        $scope.shouldShowEditingItem = shouldShowEditingItem;
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
            $scope.currentStore = store;
            $scope.resetCategoriesData();
        }


        // states
        // =====================================================================


        // =====================================================================


    });
})();
