(function(){
    'use strict';
    var app = angular.module('myApp', ['factories', 'ng.django.urls'], function config($httpProvider){
        $httpProvider.interceptors.push('AuthInterceptor');
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    });
    app.controller('myCtrl', function($scope, $http, UserFactory, CommentFactory, RateFactory, StoresFactory,
                                      CategoriesFactory, ItemsFactory){
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
        $scope.resetItemData = resetItemData;
        $scope.resetCategoriesData = resetCategoriesData;

        $scope.getCategoriesList = getCategoriesList;
        $scope.getItemsList = getItemsList;
        $scope.getItemDetails = getItemDetails;

        $scope.editItem = editItem;
        $scope.deleteItem = deleteItem;

        function noParentCategories(){
            return $scope.parentCategoriesList.length == 0;
        }


        function parentCategoryActive(category){
            return $scope.parentCategoriesList.length > 0 && category == $scope.parentCategoriesList[-1];
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
            $scope.itemsFieldState = "itemDetails";
        }

        function setCurrentCategory(category) {
            if ($scope.canShowActiveCategory){
                $scope.parentCategoriesList.pop();
            }
            $scope.cancelCreatingItem();
            $scope.cancelEditingItem();
            $scope.parentCategoriesList.push(category);
            $scope.currentCategory = category;
            $scope.resetItemData();
            $scope.getCategoriesList(category);
            $scope.itemsFieldState = '';
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

        function getCategoriesList(category){
            CategoriesFactory.getCategoriesList(category).then(function success(response){
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
                                if ($scope.categoriesList[i].id == item[0]){
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
                if ($scope.itemsList && $scope.itemsList.length > 0){
                    $scope.itemsFieldState = "itemsList";
                }
                if ($scope.itemsList){
                    for (var i = 0; i < $scope.itemsList.length; i++){
                        $scope.itemsList[i].stars = generateStarsArray($scope.itemsList[i].average_rate)
                    }
                }
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

        function resetCategoriesData(){
            $scope.categoriesList = [];
            $scope.parentCategoriesList = [];
            $scope.currentCategory = null;
            $scope.itemsFieldState = '';
            $scope.getCategoriesList();
            $scope.resetItemData();
        }

        function deleteItem(item){
            if ($scope.userIsStaff()){
                ItemsFactory.deleteItem(item).then(function success(response){
                    $scope.setCurrentCategory($scope.currentCategory);
                })
            }
            else{
                alert("You need to be logged in as staff member to delete items!");
            }

        }


        function editItem(item){
            ItemsFactory.editItem(item).then(function success(response){
                $scope.setCurrentItem(response.data);
                $scope.isEditingItem = false;
                $scope.editedItem = null;
            });
        }

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

        $scope.startCreatingItem = startCreatingItem;

        function startCreatingItem() {
            if (!$scope.userIsStaff()){
                alert("You need to be logged in as staff member to edit items!");
            }
            else if ($scope.currentStore.id == 'master'){
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

        $scope.cancelCreatingItem = cancelCreatingItem;

        function cancelCreatingItem(){
            $scope.createdItem = null;
            $scope.allCategories = null;
            $scope.isCreatingItem = false;

        }

        $scope.resetCreateItemForm = resetCreateItemForm;

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

        $scope.showCreateItemButton = showCreateItemButton;

        $scope.showEditDeleteItemButtons = showEditDeleteItemButtons;

        function showEditDeleteItemButtons(item){
            return $scope.currentStore.id == item.store && $scope.userIsStaff();
        }

        function showCreateItemButton(){
            return $scope.currentStore.id != 'master' && $scope.userIsStaff() && !$scope.createdItem;
        }


        $scope.createItem = createItem;

        function createItem(item){
            ItemsFactory.createItem(item).then(function success(response){
                $scope.setCurrentItem(response.data);
                $scope.cancelCreatingItem();
            }, handleServerError);
        }

        $scope.startEditingItem = startEditingItem;

        $scope.setAllCategories = setAllCategories;

        function setAllCategories(item){
            CategoriesFactory.setAllCategories().then(function success(response){
                $scope.allCategories = {
                    availableOptions: response.data.data
                };
                //if (item){
                //    for (var i = 0; i < $scope.allCategories.length; i++){
                //        if (item.category == $scope.allCategories[i].id){
                //            $scope.createItem.selectedOption = $scope.allCategories[i]
                //        }
                //    }
                //}
                //else{
                //    $scope.createItem.selectedOption = null;
                //}
            }, handleServerError);
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
                $scope.editedItem = Object.assign({}, item);
                $scope.setAllCategories(item);
                $scope.isEditingItem = true;
            }
        }




        $scope.cancelEditingItem = cancelEditingItem;

        function cancelEditingItem(){
            $scope.editedItem = null;
            $scope.isEditingItem = false;
            $scope.allCategories = null;
        }

        $scope.itemsFieldState = "";



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
            $scope.resetCategoriesData();
        }

    });
})();
