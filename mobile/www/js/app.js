var splashapp = angular.module('splash-app', ['ui.bootstrap']);

splashapp.config(['$httpProvider', function ($httpProvider) {

    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];
}]);

splashapp.controller('MainCtrl', function ($rootScope, $scope, $http) {
    $rootScope.serverUrl = 'http://white.jasonpang.org:5000';

    $scope.save = function () {
        $http.get($rootScope.serverUrl + '/users').
            success(function (data, status, headers, config) {
                alert(data);
                $scope.json = data;
                //$scope.json =  JSON.parse(data);
                alert($scope.json);
                alert($scope.json.users);
                alert($scope.json.users[0]);
                alert($scope.json.users[0].name);
                $scope.name = $scope.json.users[1].name;
                $scope.phone = $scope.json.users[1].phone;
                $scope.email = $scope.json.users[1].email;
            }).
            error(function (data, status, headers, config) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
                alert("There was an error.");
                alert(data);
            });
    };
});