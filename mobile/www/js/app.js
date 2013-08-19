var splashapp = angular.module('splash-app', ['ui.bootstrap']);

splashapp.config(['$httpProvider', function ($httpProvider) {

    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];
}]);

splashapp.controller('MainCtrl', function ($rootScope, $scope, $http) {
    $rootScope.serverUrl = 'http://white.jasonpang.org:5000';
    //$rootScope.serverUrl = 'http://127.0.0.1:5000';

    $scope.save = function () {
        $http.get($rootScope.serverUrl + '/user?id="er9t78vh6w4e789t6hw354786ty354').
            success(function (data, status, headers, config) {
                $scope.json = data;
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