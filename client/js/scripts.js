var app = angular.module('myApp', []);
	app.controller('myCtrl', function($scope, $http){
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
					url: 'http://localhost:8000/itemlist/' + $scope.catId,
					};
				var rez = $http(request);
					rez.success(function(data){
						$scope.items = data;
					});
					rez.error(function(data){
						alert(error + data);
					});
				}
			else{
				$scope.catId = '';
				$scope.catName='Root';
			}
		    var request = {
				method: 'GET',
				url: 'http://localhost:8000/categorylist/' + $scope.catId,
			};
			var rez = $http(request);
				rez.success(function(data){
					$scope.categories = data;
				});
				rez.error(function(data){
					alert(error + data);
				});


		}
		$scope.itemDetail = function(id){// get detail info about item from server
			var request = {
				method: 'GET',
				url: 'http://localhost:8000/itemdetail/' + id,
			};
			var rez = $http(request);
				rez.success(function(data){
					$scope.detailItem = data;
				});
				rez.error(function(data){
					alert(error + data);
				});

		}
		$scope.categoryList();

	});