var app = angular.module('myApp', []);
	app.controller('myCtrl', function($scope, $http){
		$scope.addCategory = '';
        $scope.catId = '';
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
		$scope.categoryList = function(){//список категорий
		    var request = {
				method: 'GET',
				url: 'http://localhost:8000/categorylist/' + $scope.catId,
			};
			var rez = $http(request);
				rez.success(function(data){
					alert('Категория считана');
					 $scope.categories = data;
					 console.log(data);
				});
				rez.error(function(data){
					alert(error+ data);
				});

		}
	});	