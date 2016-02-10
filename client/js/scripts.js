var app = angular.module('myApp', []);
	app.controller('myCtrl', function($scope, $http){
		$scope.addCategory = '';
        $scope.catId = '';
		$scope.a = 'three'
		$scope.categories = [];

		$scope.tree = [];
		$scope.categoryAdd = function(){//добавление категории
      		var request = {
				method: 'POST',
				url: 'http://localhost:8000/categoryadd/',
				data:{
					'name': $scope.addCategory
				}
			};
			var rez = $http(request);
			rez.success(function(data){
					alert('Категория создана');
				});
			rez.error(function(data){
					alert('error' + data);
				});
		};


		$scope.categoryList = function(id, name){//список категорий
			if(id){
				$scope.catId = id;
				$scope.catName = name;
			}
			else{
				$scope.catId = ''
			}
		    var request = {
				method: 'GET',
				url: 'http://localhost:8000/categorylist/' + $scope.catId,
			};
			var rez = $http(request);
				rez.success(function(data){
					$scope.categories = data;

					console.log(data);
				});
				rez.error(function(data){
					alert(error + data);
				});

		}
		$scope.categoryList();

	});