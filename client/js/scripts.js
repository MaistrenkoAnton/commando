var app = angular.module('myApp', []);
	app.controller('myCtrl', function($scope, $http){

		$scope.addCategory = '';

		$scope.categoryAdd = function(){//добавление категории
			// var fd = new FormData();
			// var datas = $('#category_form').serializeArray();
			// for (var i = 0; i < datas.length; i++) {
			// 	fd.append(datas[i].name, datas[i].value);
			// }
			// 	fd.append("image", $("#id_cat_img")[0].files[0]);

			var request = {
				method: 'POST',
				url: 'http://localhost:8000/categoryadd/',
				data:{
					'name': $scope.addCategory
				}
				// data: fd,
				// headers:{
				// 	'Content-Type': undefined, 
				// 	'Authorization': 'Token '+$window.sessionStorage.token
				// },
			};
			var rez = $http(request);
				rez.success(function(data){
					alert('Категория создана');
				});
				rez.error(function(data){
					console.log(data);
					alert(data.name[0]);
				});
		}
	});	