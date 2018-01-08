/*global  angular:false */
/*jslint sub: true, browser: true, indent: 4, vars: true, nomen: true */
'use strict';

// Declare app level module which depends on filters, and services
var app = angular.module('geneulike', [
    'geneulike.resources',
    'angular-carousel',
    'ngDialog',
    'ngTableToCsv',
    'ngFileUpload',
    'ngSanitize',
    'ngCookies',
    'angular-js-xlsx',
    'ngRoute','angular-venn','angularFileUpload',
    'ui.bootstrap',
    'datatables',
    'ui.tree',
    'uuid',
    'ngTable',
    'angucomplete-alt',
    'ui.select',
    ]).

config(['$routeProvider','$logProvider',
    function ($routeProvider) {
        $routeProvider.when('/', {
            templateUrl: 'views/home.html',
            controller: 'appCtrl'
        });

        $routeProvider.when('/help', {
            templateUrl: 'views/help.html',
            controller: 'noCtrl'
        });

         $routeProvider.when('/jobresults', {
            templateUrl: 'views/jobresults.html',
            controller: 'jobresultsCtrl'
        });

        $routeProvider.when('/admin', {
            templateUrl: 'views/admin.html',
            controller: 'adminCtrl'
        });

        $routeProvider.when('/query', {
            templateUrl: 'views/query.html',
            controller: 'queryCtrl'
        });

        $routeProvider.when('/about', {
            templateUrl: 'views/about.html',
            controller: 'noCtrl'
        });

        $routeProvider.when('/tools', {
            templateUrl: 'views/tools.html',
            controller: 'noCtrl'
        });

        $routeProvider.when('/jobs', {
            templateUrl: 'views/jobs.html',
            controller: 'jobsCtrl'
        });

        $routeProvider.when('/involved', {
            templateUrl: 'views/involved.html',
            controller: 'noCtrl'
        });

        $routeProvider.when('/recover', {
            templateUrl: 'views/recover.html',
            controller: 'recoverCtrl'
        });
        $routeProvider.when('/password_recover', {
            templateUrl: './views/password_recover.html',
            controller: 'passwordRecoverCtrl'
        });

        $routeProvider.when('/ontologies', {
            templateUrl: 'views/ontologies.html',
            controller: 'ontologiesCtrl'
        });

        $routeProvider.when('/compare', {
            templateUrl: 'views/compare.html',
            controller: 'compareCtrl'
        });

        $routeProvider.when('/convert', {
            templateUrl: 'views/convert.html',
            controller: 'convertCtrl'
        });

        $routeProvider.when('/search', {
            templateUrl: 'views/search.html',
            controller: 'searchCtrl'
        });

        $routeProvider.when('/tutorial', {
            templateUrl: 'views/tutorials.html',
            controller: 'noCtrl'
        });

        $routeProvider.when('/downloads', {
            templateUrl: 'views/downloads.html',
            controller: 'noCtrl'
        });

        $routeProvider.when('/browse', {
            templateUrl: 'views/browse.html',
            controller: 'browseCtrl'
        });

        $routeProvider.when('/database', {
            templateUrl: 'views/database.html',
            controller: 'databaseCtrl'
        });

        $routeProvider.when('/predict', {
            templateUrl: 'views/prediction.html',
            controller: 'noCtrl'
        });

         $routeProvider.when('/enrich', {
            templateUrl: 'views/enrich.html',
            controller: 'enrichCtrl'
        });

         $routeProvider.when('/dist', {
            templateUrl: 'views/dist.html',
            controller: 'distCtrl'
        });

        $routeProvider.when('/prio', {
            templateUrl: 'views/prio.html',
            controller: 'noCtrl'
        });

        $routeProvider.when('/signin', {
            templateUrl: 'views/signin.html',
            controller: 'signinCtrl'
        });

        $routeProvider.when('/user/:id', {
            templateUrl: 'views/user.html',
            controller: 'userInfoCtrl'
        });

        $routeProvider.when('/user/:id/myproject', {
            templateUrl: 'views/user_project.html',
            controller: 'userprojectCtrl'
        });

        $routeProvider.when('/user/:id/create_new', {
            templateUrl: 'views/create_new.html',
            controller: 'createCtrl'
        });

        $routeProvider.when('/tutorials/overview', {
            templateUrl: 'tutorial/overview.html',
            controller: 'noCtrl'
        });

         $routeProvider.when('/tutorials/register', {
            templateUrl: 'tutorial/register.html',
            controller: 'noCtrl'
        });

          $routeProvider.when('/tutorials/logging', {
            templateUrl: 'tutorial/logging.html',
            controller: 'noCtrl'
        });

           $routeProvider.when('/tutorials/spreadsheet', {
            templateUrl: 'tutorial/spreadsheet.html',
            controller: 'noCtrl'
        });

        $routeProvider.when('/tutorials/upload', {
            templateUrl: 'tutorial/upload.html',
            controller: 'noCtrl'
        });

        $routeProvider.when('/tutorials/update', {
            templateUrl: 'tutorial/update.html',
            controller: 'noCtrl'
        });

        $routeProvider.when('/tutorials/public', {
            templateUrl: 'tutorial/public.html',
            controller: 'noCtrl'
        });

        $routeProvider.when('/login', {
            templateUrl: 'views/login.html',
            controller: 'loginCtrl'
        });
       $routeProvider.otherwise({
            redirectTo: '/'
        });
}]).

config(['$httpProvider', function ($httpProvider){
    $httpProvider.interceptors.push( function($q, $window){
        return {
            'request': function (config) {
                 config.headers = config.headers || {};
                 if ($window.sessionStorage.token) {
                     config.headers.Authorization = 'Bearer ' + $window.sessionStorage.token;
                 }
                 return config;
            },
            'response': function(response){
                return response;
            },
            'responseError': function(rejection){
                if(rejection.status == 401) {
                    // Route to #/login
                    ////console.log('Rentre chez toi')
                    location.replace('#/');
                }
                return $q.reject(rejection);
            }
        };
    });
}]);

app.controller('noCtrl',
    function ($scope,$rootScope, $log, Auth, User,$location) {

});


app.controller('appCtrl',
    function ($scope,$rootScope, $log, Auth, User,$cookieStore, $location,Dataset) {
        $scope.msg = null;

        var user = Auth.getUser();
        if(user !== null && user !== undefined) {
            var cookie_selectID =  $cookieStore.get('selectedID');
           var cookie_jobID =  $cookieStore.get('jobID');
           if (cookie_selectID != undefined && cookie_selectID != ''){
            var user_seletedID = user.selectedID.split(',');
            var cookies_list = cookie_selectID.split(',');
            var job_list = cookie_jobID.split(',');

            
            for(var i=0;i<cookies_list.length; i++){
              var index = user_seletedID.indexOf(cookies_list[i]);
              if (index == -1){
                user_seletedID.push(cookies_list[i]);
              }
            }
            user.selectedID = user_seletedID.join(',');
            user.$save({'uid': user.id}).then(function(data){
                user = data;
                $cookieStore.put('selectedID',null)
            });
           }

           if (cookie_jobID != undefined && cookie_jobID != ''){
              for(var i=0;i < job_list.length; i++){
                var index = user_seletedID.indexOf(job_list[i]);
                if (index > -1){
                  user_seletedID.push(job_list[i]);
                }
              }
              user.jobID = user_seletedID.join(',');
              user.$save({'uid': user.id}).then(function(data){
                  user = data;
                  $cookieStore.put('jobID',null)
              });
           }
           
        }

        if(user === null || user === undefined) {
            User.is_authenticated({},{}).$promise.then(function(data){
                $rootScope.$broadcast('loginCtrl.login', data);
                Auth.setUser(data);
            });

        }


         
        Dataset.get({'filter':'private','collection':'projects','field':'status', 'obs':true}).$promise.then(function(data){
            $scope.last_sign = data.request;
            //console.log($scope.last_sign);
        });

        $(document).ready(function(){
  
        var $randomnbr = $('.nbr');
        var $timer= 15;
        var $it;
        var $data = 0;
        var index;
        var change;
        var letters = ["W", "e", "l", "c", "o", "m", "e", "&nbsp;", "t", "o", "&nbsp;", "G", "e", "n", "e", "U", "L", "i", "k", "e"];

  //var letters = ["W", "e", "l", "c", "o", "m", "e", "t" "o", "G", "e", "n", "e", "u", "l", "i", "k", "e"];
  
        $randomnbr.each(function(){
      
        change = Math.round(Math.random()*100);
        $(this).attr('data-change', change);
    
        });
  
        function random(){
            return Math.round(Math.random()*9);
        };
  
        function select(){
            return Math.round(Math.random()*$randomnbr.length+1);
        };
  
        function value(){
            $('.nbr:nth-child('+select()+')').html(''+random()+'');
            $('.nbr:nth-child('+select()+')').attr('data-number', $data);
            $data++;
    
            $randomnbr.each(function(){
            if(parseInt($(this).attr('data-number')) > parseInt($(this).attr('data-change'))){
                index = $('.ltr').index(this);
                $(this).html(letters[index]);
                $(this).removeClass('nbr');
            }
            });
    
        };
  
        $it = setInterval(value, $timer);
    
});

        // var text = $(".split");

        // var split = new SplitText(text);

        // function random(min, max){
        //     return (Math.random() * (max - min)) + min;
        // }

        // $(split.chars).each(function(i){
        // TweenMax.from($(this), 2.5, {
        // opacity: 0,
        // x: random(-500, 500),
        // y: random(-500, 500),
        // z: random(-500, 500),
        // scale: .1,
        // delay: i * .02,
        // yoyo: true,
        // repeat: false,
        // repeatDelay: 10
        // });
        // });   


        //INSERT FUNCTION GET LAST
        //Get last updated signature on TOXsIgN

});

app.controller('queryCtrl',
    function ($scope,$rootScope, Auth, User, Dataset, Search, $filter, ngTableParams) {
        $scope.selected_type = '';
        $scope.selected_field = {};
        $scope.search_history = [];
        $scope.selected_querymode = {};
        $scope.research = '';
        $scope.query = {};
        $scope.querymode = '';

        $scope.pfrom=0;
        $scope.sfrom=0;
        $scope.stfrom=0;
        $scope.lfrom=0;

        $scope.selected_field.projects='';
        $scope.selected_field.studies='';
        $scope.selected_field.strategies='';
        $scope.selected_field.lists='';


        $scope.param_add = function() {
          // console.log($scope.selected_field);
          // console.log($scope.selected_type);

            number_query +=1
            console.log("number_query");
            console.log(number_query);
            if($scope.research == ''){
                $scope.research="*";
            }
            else{
              $scope.research ="*"+$scope.research+"*";
            }

            if($scope.selected_type == 'projects'){

                if ($scope.selected_field.projects == ''){
                    var value = '(_type:'+$scope.selected_type+' AND '+'_all'+':'+$scope.research+')';
                    //var value=[{'_type': str($scope.selected_type)}, {'selector' : 'AND'}, {'field': '_all', {'search' : str($scope.research)}}]
                }
                else{
                    var value = '(_type:'+$scope.selected_type+' AND '+$scope.selected_field.projects+':'+$scope.research+')';            
                }
            }
            else if($scope.selected_type == 'studies'){
                if($scope.selected_field.studies == ''){
                    var value = '(_type:'+$scope.selected_type+' AND '+'_all'+':'+$scope.research+')';
                }
                else{
                    var value = '(_type:'+$scope.selected_type+' AND '+$scope.selected_field.studies+':'+$scope.research+')';  
                }
                
            }
            else if($scope.selected_type == 'strategies'){

                if($scope.selected_field.strategies== ''){
                    var value = '(_type:'+$scope.selected_type+' AND '+'_all'+':'+$scope.research+')';
                    
                }
                else{
                    var value = '(_type:'+$scope.selected_type+' AND '+$scope.selected_field.strategies+':'+$scope.research+')';
                }
            }
            else if($scope.selected_type == 'lists'){

                if($scope.selected_field.lists== ''){
                    var value = '(_type:'+$scope.selected_type+' AND '+'_all'+':'+$scope.research+')';
                    
                }
                else{
                    var value = '(_type:'+$scope.selected_type+' AND '+$scope.selected_field.lists+':'+$scope.research+')';
                }
            }
            else if($scope.selected_type == '_all'){
              // console.log("we are here");
                var value = '(_all:'+$scope.research+')';
                // console.log(value);
            }

            // console.log(value);
            // console.log($scope.selected_field);
            if($scope.selected_querymode.mode == undefined){
              console.log("ADD to dico");
              $scope.query[value] = 'AND';
              $scope.selected_querymode.mode = 'AND';
            }
            else {
              $scope.query[value] = $scope.selected_querymode.mode;
            }
            $scope.selected_type = '';
            $scope.selected_field = {};
            $scope.research = '';
            $scope.selected_field.projects='';
            $scope.selected_field.studies='';
            $scope.selected_field.strategies='';
            $scope.selected_field.lists='';

        };
        // $scope.param_add = function() {
        //   console.log($scope.selected_field);
        //     if($scope.selected_type == 'projects'){
        //       var value = '(_type:'+$scope.selected_type+' AND '+$scope.selected_field.projects+':'+$scope.research+')';
        //     }
        //     if($scope.selected_type == 'studies'){
        //       var value = '(_type:'+$scope.selected_type+' AND '+$scope.selected_field.studies+':'+$scope.research+')';
        //     }
        //     if($scope.selected_type == 'signatures'){
        //       var value = '(_type:'+$scope.selected_type+' AND '+$scope.selected_field.signatures+':'+$scope.research+')';
        //     }
        //      if($scope.selected_type == 'all'){
        //       var value = $scope.research;
        //     }
        //     console.log(value);
        //     console.log($scope.selected_field);
        //     if($scope.selected_querymode.mode == undefined){
        //       console.log("ADD to dico");
        //       $scope.query[value] = 'AND';
        //       $scope.selected_querymode.mode = 'AND';
        //     }
        //     else {
        //       $scope.query[value] = $scope.selected_querymode.mode;
        //     }
        //     $scope.selected_type = '';
        //     $scope.selected_field = {};
        //     $scope.research = '';

        // };

        $scope.search_history_item = function(item) {
            $scope.query = item;
            $scope.search(false);
        }

        $scope.more = function(type){
            if(type == 'projects'){
                $scope.pfrom=$scope.pfrom+24
            }
            else if(type == 'studies'){
                $scope.sfrom=$scope.sfrom+24       
            }
            else if(type == 'strategies'){
                $scope.stfrom= $scope.stfrom+24
            }
            else{
                $scope.lfrom=$scope.lfrom+24   
              }
            
            var query_piece = '';//'status:public ';
            for(var filter in $scope.query){
                query_piece = query_piece +$scope.query[filter]+' '+filter+' ';
            }

            query_piece=query_piece.substr(4);
                // console.log(query_piece);
            console.log(query_piece);
            Search.search_index({"query":query_piece, 'query_dico':$scope.query,'number_query':number_query, 'pfrom':$scope.pfrom, 'sfrom':$scope.sfrom, 'stfrom':$scope.sgfrom, 'lfrom' : $scope.lfrom}).$promise.then(function(data){
                console.log("OKKKKK");
                console.log(data);
                console.log(number_query);
                console.log(data['query'] == '(_all:*) ');
                if(data['query'] == '(_all:*) ' ){
                    console.log("here");
                    $location.path('/database'); 
                }

                  // }

                else if (data['number_query'] == '1'){
                    console.log("=====1")
                    console.log(data);
                    $scope.projects = [];
                    $scope.studies = [];
                    $scope.strategies = [];
                    $scope.lists=[];
                    $scope.search_results = data['page'];
                    $scope.results = $scope.search_results.hits.hits;

                    if (query_piece.includes('projects') && data['number'] != 0){
                        $scope.projects_number= ''+data['number'];
                        $scope.studies_number = 'No Result';
                        $scope.strategies_number = 'No Result';
                        $scope.lists_number = 'No Result';
                        for(var i =0;i<$scope.results.length;i++){
                            $scope.projects.push($scope.results[i]['_source']);
                        }
                    }

                    else if(query_piece.includes('studies') && data['number'] != 0){
                        $scope.studies_number= data['number'];
                        $scope.projects_number = 'No Result';
                        $scope.strategies_number = 'No Result';
                        $scope.lists_number = 'No Result'; 
                        for(var i =0;i<$scope.results.length;i++){
                            $scope.studies.push($scope.results[i]['_source']);
                        }
                    }

                    else if(query_piece.includes('strategies') && data['number'] != 0){
                        $scope.strategies_number= data['number'];
                        $scope.projects_number = 'No Result';
                        $scope.studies_number = 'No Result';
                        $scope.lists_number = 'No Result';
                        for(var i =0;i<$scope.results.length;i++){
                            $scope.strategies.push($scope.results[i]['_source']);
                        }
                    }

                    else if(query_piece.includes('lists') && data['number'] != 0){
                        $scope.lists_number= data['number'];
                        $scope.projects_number = 'No Result';
                        $scope.studies_number = 'No Result';
                        $scope.strategies_number = 'No Result';
                        for(var i =0;i<$scope.results.length;i++){
                            $scope.lists.push($scope.results[i]['_source']);
                        }
                    }
                    
                    else{
                        $scope.lists_number= 'No Result';
                        $scope.projects_number = 'No Result';
                        $scope.studies_number = 'No Result';
                        $scope.strategies_number = 'No Result';
                    }


                      // for(var i =0;i<$scope.results.length;i++){
                      //   if($scope.results[i]['_type'] == 'projects'){
                      //     $scope.projects.push($scope.results[i]['_source']);
                      //   //$scope.project_number ++;
                      //   }
                      //   if($scope.results[i]['_type'] == 'studies'){
                      //     $scope.studies.push($scope.results[i]['_source']);
                      //   //$scope.studies_number ++;
                      //   }
                      //   if($scope.results[i]['_type'] == 'strategies'){
                      //     $scope.signatures.push($scope.results[i]['_source']);
                      //   //$scope.signatures_number ++;
                      //   }

                      // }

                    }
                    else{



                        $scope.projects = [];
                        $scope.studies = [];
                        $scope.strategies = [];
                        $scope.lists = [];
                        $scope.results="true";

                        $scope.projects_number = data['number_project'];
                        $scope.studies_number=  data['number_study'];                  
                        $scope.strategies_number = data['number_study'];
                        $scope.lists_number=data['number_list'];


                        if (data['projects'] != null){
                            $scope.search_projects = data['projects'].hits.hits;
                            for(var i =0;i<$scope.search_projects.length;i++){
                                $scope.projects.push($scope.search_projects[i]['_source']);
                            }
                        }
                        else{
                            $scope.projects_number="No Result";
                        }

                        if (data['studies'] != null){
                            $scope.search_studies = data['studies'].hits.hits;
                            for(var i =0;i<$scope.search_studies.length;i++){
                                $scope.studies.push($scope.search_studies[i]['_source']);
                            }
                        }
                        else{
                            $scope.studies_number="No Result";
                        }


                        if (data['strategies'] != null){
                            $scope.search_signatures = data['strategies'].hits.hits;
                            for(var i =0;i<$scope.search_strategies.length;i++){
                                $scope.strategies.push($scope.search_strategies[i]['_source']);
                            }
                        }
                        else{
                            $scope.strategies_number="No Result";
                        }

                        if (data['lists'] != null){
                            $scope.search_lists = data['lists'].hits.hits;
                            for(var i =0;i<$scope.search_lists.length;i++){
                                $scope.lists.push($scope.search_lists[i]['_source']);
                            }
                        }
                        else{
                            $scope.lists_number="No Result";
                        }

                        console.log($scope.projects);
                        console.log($scope.studies);
                        console.log($scope.signatures);


                    }

            });

        };
        $scope.back = function(type){



            if(type == 'projects'){
                $scope.pfrom=$scope.pfrom-24
            }
            else if(type == 'studies'){
                $scope.sfrom=$scope.sfrom-24       
            }
            else if(type == 'strategies'){
                $scope.stfrom= $scope.stfrom-24
            }
            else{
                $scope.lfrom=$scope.lfrom-24   
              }
            
            var query_piece = '';//'status:public ';
            for(var filter in $scope.query){
                query_piece = query_piece +$scope.query[filter]+' '+filter+' ';
            }

            query_piece=query_piece.substr(4);
                // console.log(query_piece);
            console.log(query_piece);
            Search.search_index({"query":query_piece, 'query_dico':$scope.query,'number_query':number_query, 'pfrom':$scope.pfrom, 'sfrom':$scope.sfrom, 'stfrom':$scope.sgfrom, 'lfrom' : $scope.lfrom}).$promise.then(function(data){
                console.log("OKKKKK");
                console.log(data);
                console.log(number_query);
                console.log(data['query'] == '(_all:*) ');
                if(data['query'] == '(_all:*) ' ){
                    console.log("here");
                    $location.path('/database'); 
                }

                  // }

                else if (data['number_query'] == '1'){
                    console.log("=====1")
                    console.log(data);
                    $scope.projects = [];
                    $scope.studies = [];
                    $scope.strategies = [];
                    $scope.lists=[];
                    $scope.search_results = data['page'];
                    $scope.results = $scope.search_results.hits.hits;

                    if (query_piece.includes('projects') && data['number'] != 0){
                        $scope.projects_number= ''+data['number'];
                        $scope.studies_number = 'No Result';
                        $scope.strategies_number = 'No Result';
                        $scope.lists_number = 'No Result';
                        for(var i =0;i<$scope.results.length;i++){
                            $scope.projects.push($scope.results[i]['_source']);
                        }
                    }

                    else if(query_piece.includes('studies') && data['number'] != 0){
                        $scope.studies_number= data['number'];
                        $scope.projects_number = 'No Result';
                        $scope.strategies_number = 'No Result';
                        $scope.lists_number = 'No Result'; 
                        for(var i =0;i<$scope.results.length;i++){
                            $scope.studies.push($scope.results[i]['_source']);
                        }
                    }

                    else if(query_piece.includes('strategies') && data['number'] != 0){
                        $scope.strategies_number= data['number'];
                        $scope.projects_number = 'No Result';
                        $scope.studies_number = 'No Result';
                        $scope.lists_number = 'No Result';
                        for(var i =0;i<$scope.results.length;i++){
                            $scope.strategies.push($scope.results[i]['_source']);
                        }
                    }

                    else if(query_piece.includes('lists') && data['number'] != 0){
                        $scope.lists_number= data['number'];
                        $scope.projects_number = 'No Result';
                        $scope.studies_number = 'No Result';
                        $scope.strategies_number = 'No Result';
                        for(var i =0;i<$scope.results.length;i++){
                            $scope.lists.push($scope.results[i]['_source']);
                        }
                    }
                    
                    else{
                        $scope.lists_number= 'No Result';
                        $scope.projects_number = 'No Result';
                        $scope.studies_number = 'No Result';
                        $scope.strategies_number = 'No Result';
                    }


                      // for(var i =0;i<$scope.results.length;i++){
                      //   if($scope.results[i]['_type'] == 'projects'){
                      //     $scope.projects.push($scope.results[i]['_source']);
                      //   //$scope.project_number ++;
                      //   }
                      //   if($scope.results[i]['_type'] == 'studies'){
                      //     $scope.studies.push($scope.results[i]['_source']);
                      //   //$scope.studies_number ++;
                      //   }
                      //   if($scope.results[i]['_type'] == 'strategies'){
                      //     $scope.signatures.push($scope.results[i]['_source']);
                      //   //$scope.signatures_number ++;
                      //   }

                      // }

                    }
                    else{



                        $scope.projects = [];
                        $scope.studies = [];
                        $scope.strategies = [];
                        $scope.lists = [];
                        $scope.results="true";

                        $scope.projects_number = data['number_project'];
                        $scope.studies_number=  data['number_study'];                  
                        $scope.strategies_number = data['number_study'];
                        $scope.lists_number=data['number_list'];


                        if (data['projects'] != null){
                            $scope.search_projects = data['projects'].hits.hits;
                            for(var i =0;i<$scope.search_projects.length;i++){
                                $scope.projects.push($scope.search_projects[i]['_source']);
                            }
                        }
                        else{
                            $scope.projects_number="No Result";
                        }

                        if (data['studies'] != null){
                            $scope.search_studies = data['studies'].hits.hits;
                            for(var i =0;i<$scope.search_studies.length;i++){
                                $scope.studies.push($scope.search_studies[i]['_source']);
                            }
                        }
                        else{
                            $scope.studies_number="No Result";
                        }


                        if (data['strategies'] != null){
                            $scope.search_signatures = data['strategies'].hits.hits;
                            for(var i =0;i<$scope.search_strategies.length;i++){
                                $scope.strategies.push($scope.search_strategies[i]['_source']);
                            }
                        }
                        else{
                            $scope.strategies_number="No Result";
                        }

                        if (data['lists'] != null){
                            $scope.search_lists = data['lists'].hits.hits;
                            for(var i =0;i<$scope.search_lists.length;i++){
                                $scope.lists.push($scope.search_lists[i]['_source']);
                            }
                        }
                        else{
                            $scope.lists_number="No Result";
                        }

                        console.log($scope.projects);
                        console.log($scope.studies);
                        console.log($scope.signatures);


                    }

          // $scope.max = $scope.max - 100;
          // var query_piece = 'status:public ';
          //   for(var filter in $scope.query){
          //       query_piece = query_piece +$scope.query[filter]+' '+filter+' '
          //     //console.log($scope.parameters[i]);
          //   }
          //   //console.log(query_piece)
          // Search.search_index({"query":query_piece,'from':$scope.max}).$promise.then(function(data){
          //       $scope.search_results = data;
          //       $scope.chemicalList = [];
          //       $scope.check = []
                
          //       $scope.signatures = []
          //       $scope.results = $scope.search_results.hits.hits;
          //       for(var i=0;i<$scope.results.length;i++){
          //         var checkd = $scope.signatures.indexOf($scope.results[i]._source);
          //         if(checkd === -1) {
          //           $scope.signatures.push($scope.results[i]._source);
          //         }

          //       }
                ////console.log($scope.signatures);
                ////console.log($scope.results._source.studies.id);
                ////console.log($scope.results._source.studies[0].id);
            });

        };



        $scope.convert_timestamp_to_date = function(UNIX_timestamp){
          if(UNIX_timestamp=='' || UNIX_timestamp===null || UNIX_timestamp===undefined) { return '';}
          var a = new Date(UNIX_timestamp*1000);
          var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
          var year = a.getFullYear();
          var month = months[a.getMonth()];
          var date = a.getDate();
          var hour = a.getHours();
          var min = a.getMinutes();
          var sec = a.getSeconds();
          var time = date + ',' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
          return time;
        };
        $scope.param_del = function(key) {
            delete $scope.query[key];
        };

        $scope.search_history_item = function(item) {
            $scope.parameters = item;
            $scope.search(false);
        }


        $scope.search = function(do_save) {
            if(do_save) {
                $scope.search_history.push(JSON.parse(JSON.stringify($scope.query)));
            }


            var query_piece = '';//'status:public ';
            for(var filter in $scope.query){
                query_piece = query_piece +$scope.query[filter]+' '+filter+' ';
            }

            query_piece=query_piece.substr(4);
                // console.log(query_piece);
            console.log(query_piece);
            Search.search_index({"query":query_piece, 'query_dico':$scope.query,'number_query':number_query, 'pfrom':$scope.pfrom, 'sfrom':$scope.sfrom, 'stfrom':$scope.sgfrom, 'lfrom' : $scope.lfrom}).$promise.then(function(data){
                console.log("OKKKKK");
                console.log(data);
                console.log(number_query);
                console.log(data['query'] == '(_all:*) ');
                if(data['query'] == '(_all:*) ' ){
                    console.log("here");
                    $location.path('/database'); 
                }

                  // }

                else if (data['number_query'] == '1'){
                    console.log("=====1")
                    console.log(data);
                    $scope.projects = [];
                    $scope.studies = [];
                    $scope.strategies = [];
                    $scope.lists=[];
                    $scope.search_results = data['page'];
                    $scope.results = $scope.search_results.hits.hits;

                    if (query_piece.includes('projects') && data['number'] != 0){
                        $scope.projects_number= ''+data['number'];
                        $scope.studies_number = 'No Result';
                        $scope.strategies_number = 'No Result';
                        $scope.lists_number = 'No Result';
                        for(var i =0;i<$scope.results.length;i++){
                            $scope.projects.push($scope.results[i]['_source']);
                        }
                    }

                    else if(query_piece.includes('studies') && data['number'] != 0){
                        $scope.studies_number= data['number'];
                        $scope.projects_number = 'No Result';
                        $scope.strategies_number = 'No Result';
                        $scope.lists_number = 'No Result'; 
                        for(var i =0;i<$scope.results.length;i++){
                            $scope.studies.push($scope.results[i]['_source']);
                        }
                    }

                    else if(query_piece.includes('strategies') && data['number'] != 0){
                        $scope.strategies_number= data['number'];
                        $scope.projects_number = 'No Result';
                        $scope.studies_number = 'No Result';
                        $scope.lists_number = 'No Result';
                        for(var i =0;i<$scope.results.length;i++){
                            $scope.strategies.push($scope.results[i]['_source']);
                        }
                    }

                    else if(query_piece.includes('lists') && data['number'] != 0){
                        $scope.lists_number= data['number'];
                        $scope.projects_number = 'No Result';
                        $scope.studies_number = 'No Result';
                        $scope.strategies_number = 'No Result';
                        for(var i =0;i<$scope.results.length;i++){
                            $scope.lists.push($scope.results[i]['_source']);
                        }
                    }
                    
                    else{
                        $scope.lists_number= 'No Result';
                        $scope.projects_number = 'No Result';
                        $scope.studies_number = 'No Result';
                        $scope.strategies_number = 'No Result';
                    }

                }
                else{



                    $scope.projects = [];
                    $scope.studies = [];
                    $scope.strategies = [];
                    $scope.lists = [];
                    $scope.results="true";

                    $scope.projects_number = data['number_project'];
                    $scope.studies_number=  data['number_study'];                  
                    $scope.strategies_number = data['number_study'];
                    $scope.lists_number=data['number_list'];


                    if (data['projects'] != null){
                        $scope.search_projects = data['projects'].hits.hits;
                        for(var i =0;i<$scope.search_projects.length;i++){
                            $scope.projects.push($scope.search_projects[i]['_source']);
                        }
                    }
                    else{
                        $scope.projects_number="No Result";
                    }

                    if (data['studies'] != null){
                        $scope.search_studies = data['studies'].hits.hits;
                        for(var i =0;i<$scope.search_studies.length;i++){
                            $scope.studies.push($scope.search_studies[i]['_source']);
                        }
                    }
                    else{
                        $scope.studies_number="No Result";
                    }


                    if (data['strategies'] != null){
                        $scope.search_signatures = data['strategies'].hits.hits;
                        for(var i =0;i<$scope.search_strategies.length;i++){
                            $scope.strategies.push($scope.search_strategies[i]['_source']);
                        }
                    }
                    else{
                        $scope.strategies_number="No Result";
                    }

                    if (data['lists'] != null){
                        $scope.search_lists = data['lists'].hits.hits;
                        for(var i =0;i<$scope.search_lists.length;i++){
                            $scope.lists.push($scope.search_lists[i]['_source']);
                        }
                    }
                    else{
                        $scope.lists_number="No Result";
                    }

                    console.log($scope.projects);
                    console.log($scope.studies);
                    console.log($scope.signatures);


                }
            });
};















        //     var query_piece = 'status:public ';
        //     for(var filter in $scope.query){
        //         query_piece = query_piece +$scope.query[filter]+' '+filter+' '
        //       //console.log($scope.parameters[i]);
        //     }
        //     console.log(query_piece)
        //     Search.search_index({"query":query_piece,'from':0}).$promise.then(function(data){
        //         $scope.projects = [];
        //         $scope.studies = [];
        //         $scope.assays = [];
        //         $scope.signatures = [];
        //         $scope.project_number = 0
        //         $scope.studies_number = 0
        //         $scope.assay_number = 0
        //         $scope.signatures_number = 0
        //         $scope.search_results = data;
        //         console.log(data);
        //         $scope.results = $scope.search_results.hits.hits;
        //         console.log($scope.results);
        //         console.log($scope.search_results.hits);

        //         for(var i =0;i<$scope.results.length;i++){
        //           if($scope.results[i]['_type'] == 'projects'){
        //             $scope.projects.push($scope.results[i]['_source']);
        //             $scope.project_number ++;
        //           }
        //           if($scope.results[i]['_type'] == 'studies'){
        //             $scope.studies.push($scope.results[i]['_source']);
        //             $scope.studies_number ++;
        //           }
        //           if($scope.results[i]['_type'] == 'assays'){
        //             $scope.assays.push($scope.results[i]['_source']);
        //             $scope.assay_number ++;
        //           }
        //           if($scope.results[i]['_type'] == 'signatures'){
        //             $scope.signatures.push($scope.results[i]['_source']);
        //             $scope.signatures_number ++;
        //           }

        //         }
        //         console.log($scope.results);
        //     });
        // }
});

app.controller('searchCtrl',
    function($scope, $rootScope, $routeParams, $log, $location, $window, User, Auth, SearchHits) {
        var hits = SearchHits.getHits();
        console.log(hits)
        $scope.nb_match = hits.hits.total
        $scope.search_result = hits.hits.hits;
        console.log($scope.search_result);
        $scope.projects = [];
        $scope.studies = [];
        $scope.assays = [];
        $scope.signatures = [];
        $scope.project_number = 0
        $scope.studies_number = 0
        $scope.assay_number = 0
        $scope.signatures_number = 0

        for(var i =0;i<$scope.search_result.length;i++){
          if($scope.search_result[i]['_type'] == 'projects'){
            $scope.projects.push($scope.search_result[i]['_source']);
            $scope.project_number ++;
          }
          if($scope.search_result[i]['_type'] == 'studies'){
            $scope.studies.push($scope.search_result[i]['_source']);
            $scope.studies_number ++;
          }
          if($scope.search_result[i]['_type'] == 'assays'){
            $scope.assays.push($scope.search_result[i]['_source']);
            $scope.assay_number ++;
          }
          if($scope.search_result[i]['_type'] == 'signatures'){
            $scope.signatures.push($scope.search_result[i]['_source']);
            $scope.signatures_number ++;
          }

        }

});

app.controller('distCtrl',
    function ($scope,$rootScope, $log, Auth, User, Dataset, $window,$cookieStore, $location) {
        $scope.msg = "Dashboard Tools";

        $scope.user = null
        $scope.user = Auth.getUser();

        if($window.sessionStorage.token) {
            $scope.token = $window.sessionStorage.token;
        }

        $scope.signatures = [];
        $scope.selected = ""
        $scope.msg = "Dashboard Tools";
        $scope.filter ="pvalue";
        $scope.adjust_filter ="lt";
        $scope.value_filter =0.01;
        $scope.job_name = "";
        $scope.resultGo="";
        $scope.labels = [];
        $scope.series = [];
        $scope.filter_val = {};
        $scope.size = 0;
        console.log($scope.user);

      $scope.add = function(){
        $scope.filter_val[$scope.filter]={'param':$scope.adjust_filter,'value':$scope.value_filter,'name':$scope.job_name};
        $scope.filter ="pvalue";
        $scope.adjust_filter ="lt";
        $scope.value_filter =0.01;
        $scope.job_name = ""
        $scope.size = Object.keys($scope.filter_val).length;

      };

       $scope.param_del = function(key) {

          delete $scope.filter_val[key];
          $scope.size = Object.keys($scope.filter_val).length;
      };

      if($scope.user == undefined || $scope.user == null){
        $scope.selected = $cookieStore.get('selectedID').split(',');
      }
      else{
        $scope.selected = $scope.user.selectedID.split(',');
        console.log($scope.selected);
      }
      for(var i=0;i<$scope.selected.length;i++){
          console.log($scope.selected[i]);
          console.log(i);
          Dataset.get({'filter':$scope.selected[i],'from':'None','to': 'None','collection':'signatures','field':'id'}).$promise.then(function(data){
            if(data.request != undefined){
              $scope.signatures.push(data.request);
            }
            console.log($scope.signatures);
          });
        }

      $scope.run = function(signature){
        var user_id = "";
        if ($scope.user != null){
          user_id = $scope.user.id;
        }
        else {
          user_id = "None"
        }
        var args =  $scope.filter+','+$scope.adjust_filter+','+$scope.value_filter
        Dataset.run({'uid':user_id, 'signature':signature, 'tool':'distance analysis', 'arguments':args,'name':$scope.job_name}).$promise.then(function(data){
          console.log(data);
          if ($scope.user != null){
            if ($scope.user.jobID == undefined){
              $scope.user.jobID = "";
            }
            var list_jobID = $scope.user.jobID.split(',');
            list_jobID.push(data.id);
            $scope.user.jobID = list_jobID.join(',');
            $scope.user.$save({'uid': $scope.user.id}).then(function(data){
              $scope.user = data;
            });
          }
          else {
            if ($cookieStore.get('jobID') != undefined){
              var list_jobID = $cookieStore.get('jobID').split(',');
            } else{
              var list_jobID = [];
            }
            list_jobID.push(data.id);
            $cookieStore.put('jobID',list_jobID.join(','));
          }
          $location.path('/jobs');;
        });
      }

});


app.controller('enrichCtrl',
    function ($scope,$rootScope, $log, Auth, User, Dataset, $location,$window,$cookieStore, ngTableParams, $filter) {
      $scope.msg = "Dashboard Tools";

        $scope.user = null
        $scope.user = Auth.getUser();

        if($window.sessionStorage.token) {
            $scope.token = $window.sessionStorage.token;
        }

        $scope.signatures = [];
        $scope.selected = ""
        $scope.msg = "Dashboard Tools";
        $scope.filter ="pvalue";
        $scope.adjust_filter ="lt";
        $scope.value_filter =0.01;
        $scope.job_name = "";
        $scope.resultGo="";
        $scope.labels = [];
        $scope.series = [];
        $scope.filter_val = {};
        $scope.size = 0;
        console.log($scope.user);

      $scope.add = function(){
        $scope.filter_val[$scope.filter]={'param':$scope.adjust_filter,'value':$scope.value_filter,'name':$scope.job_name};
        $scope.filter ="pvalue";
        $scope.adjust_filter ="lt";
        $scope.value_filter =0.01;
        $scope.job_name = ""
        $scope.size = Object.keys($scope.filter_val).length;

      };

       $scope.param_del = function(key) {

          delete $scope.filter_val[key];
          $scope.size = Object.keys($scope.filter_val).length;
      };

      if($scope.user == undefined || $scope.user == null){
        $scope.selected = $cookieStore.get('selectedID').split(',');
      }
      else{
        $scope.selected = $scope.user.selectedID.split(',');
        console.log($scope.selected);
      }
      for(var i=0;i<$scope.selected.length;i++){
          console.log($scope.selected[i]);
          console.log(i);
          Dataset.get({'filter':$scope.selected[i],'from':'None','to': 'None','collection':'signatures','field':'id'}).$promise.then(function(data){
            if(data.request != undefined){
              $scope.signatures.push(data.request);
            }
            console.log($scope.signatures);
          });
        }

      $scope.run = function(signature){
        var user_id = "";
        if ($scope.user != null){
          user_id = $scope.user.id;
        }
        else {
          user_id = "None"
        }
        var args =  $scope.filter+','+$scope.adjust_filter+','+$scope.value_filter
        Dataset.run({'uid':user_id, 'signature':signature, 'tool':'functional analysis', 'arguments':args,'name':$scope.job_name}).$promise.then(function(data){
          console.log(data);
          if ($scope.user != null){
            if ($scope.user.jobID == undefined){
              $scope.user.jobID = "";
            }
            var list_jobID = $scope.user.jobID.split(',');
            list_jobID.push(data.id);
            $scope.user.jobID = list_jobID.join(',');
            $scope.user.$save({'uid': $scope.user.id}).then(function(data){
              $scope.user = data;
            });
          }
          else {
            if ($cookieStore.get('jobID') != undefined){
              var list_jobID = $cookieStore.get('jobID').split(',');
            } else{
              var list_jobID = [];
            }
            list_jobID.push(data.id);
            $cookieStore.put('jobID',list_jobID.join(','));
          }
          $location.path('/jobs');;
        });
      }

});

app.controller('jobresultsCtrl',
    function ($scope,$rootScope, $log, Auth, User, Dataset, $location, ngTableParams, $filter) {

      var params = $location.search();
      Dataset.getjob({'job_list':"",'jid':params['job']}).$promise.then(function(data){
        $scope.job = data.jobs;
        console.log($scope.job);
        Dataset.readresult({'job':$scope.job.id}).$promise.then(function(datas){
          $scope.resultcc = datas.results;
          $scope.Math = window.Math;
          if ($scope.job.tool == 'distance analysis'){
            $scope.conditionTable = new ngTableParams({
              page: 1,
              count: 50,
          },
           {
              total: $scope.resultcc.length,
              getData: function ($defer, params) {
                  $scope.datacc = params.sorting() ? $filter('orderBy')($scope.resultcc, params.orderBy()) : $scope.resultcc;
                  $scope.datacc = params.filter() ? $filter('filter')($scope.datacc, params.filter()) : $scope.datacc;
                  $scope.datacc = $scope.datacc.slice((params.page() - 1) * params.count(), params.page() * params.count());
                  $defer.resolve($scope.datacc);
              }
          });

          }
          if ($scope.job.tool == 'functional analysis'){
            $scope.resultGo = datas.Bp;
                console.log(datas);
                $scope.conditionTable = new ngTableParams({
                    page: 1,
                    count: 50,
                },
                 {
                    total: $scope.resultGo.length,
                    getData: function ($defer, params) {
                        $scope.data = params.sorting() ? $filter('orderBy')($scope.resultGo, params.orderBy()) : $scope.resultGo;
                        $scope.data = params.filter() ? $filter('filter')($scope.data, params.filter()) : $scope.data;
                        $scope.data = $scope.data.slice((params.page() - 1) * params.count(), params.page() * params.count());
                        $defer.resolve($scope.data);
                    }
                });

                $scope.resultMF = datas.Mf;
                $scope.MfTable = new ngTableParams({
                    page: 1,
                    count: 50,
                },
                 {
                    total: $scope.resultMF.length,
                    getData: function ($defer, params) {
                        $scope.datamf = params.sorting() ? $filter('orderBy')($scope.resultMF, params.orderBy()) : $scope.resultMF;
                        $scope.datamf = params.filter() ? $filter('filter')($scope.datamf, params.filter()) : $scope.datamf;
                        $scope.datamf = $scope.datamf.slice((params.page() - 1) * params.count(), params.page() * params.count());
                        $defer.resolve($scope.datamf);
                    }
                });

                $scope.resultcc = datas.Cc;
                $scope.ccTable = new ngTableParams({
                    page: 1,
                    count: 50,
                },
                 {
                    total: $scope.resultcc.length,
                    getData: function ($defer, params) {
                        $scope.datacc = params.sorting() ? $filter('orderBy')($scope.resultcc, params.orderBy()) : $scope.resultcc;
                        $scope.datacc = params.filter() ? $filter('filter')($scope.datacc, params.filter()) : $scope.datacc;
                        $scope.datacc = $scope.datacc.slice((params.page() - 1) * params.count(), params.page() * params.count());
                        $defer.resolve($scope.datacc);
                    }
                });

                $scope.resultds = datas.Disease;
                $scope.dsTable = new ngTableParams({
                    page: 1,
                    count: 50,
                },
                 {
                    total: $scope.resultds.length,
                    getData: function ($defer, params) {
                        $scope.datads = params.sorting() ? $filter('orderBy')($scope.resultds, params.orderBy()) : $scope.resultds;
                        $scope.datads = params.filter() ? $filter('filter')($scope.datads, params.filter()) : $scope.datads;
                        $scope.datads = $scope.datads.slice((params.page() - 1) * params.count(), params.page() * params.count());
                        $defer.resolve($scope.datads);
                    }
                });

          }
          
        });

      });


      $scope.get_Info = function(id){
        Dataset.get({'filter':id,'from':'None','to':'None','collection':'signatures','field':'id'}).$promise.then(function(result){
          var name = "";
          name = result.request.title;
          console.log(name);
          return name;
        });
      }

      $scope.show_dataset = function(id){
        $location.url('/browse?dataset='+id);
      };

      
     

});





app.controller('convertCtrl',
    function ($scope,$rootScope, $log, Auth, User, Dataset, $window, $cookieStore, Upload, $location) {
        
        $scope.showGPL = function(){
            if($scope.selectFrom == "GPL"){
                return $scope.showFrom=true;
            }

        };

         $scope.GPLnnnannot = false;
         $scope.GPL1nnnannot = false;
        $scope.GPL2nnnannot = false;
        $scope.GPL3nnnannot = false;
        $scope.GPL4nnnannot = false;
        $scope.GPL5nnnannot = false;
        $scope.GPL6nnnannot = false;
        $scope.GPL7nnnannot = false;
        $scope.GPL8nnnannot = false;
        $scope.GPL9nnnannot = false;
        $scope.GPL10nnnannot = false;
        $scope.GPL11nnnannot = false;
        $scope.GPL12nnnannot = false;
        $scope.GPL13nnnannot = false;
        $scope.GPL14nnnannot = false;
        $scope.GPL15nnnannot = false;
        $scope.GPL16nnnannot = false;
        $scope.GPL17nnnannot = false;
        $scope.selectGPL = function(){
            if($scope.select.GPL == "GPLnnn"){
                return $scope.GPLnnnannot= true
            }
            else if($scope.select.GPL == "GPL1nnn"){
                return $scope.GPL1nnnannot= true;
            }
            else if($scope.select.GPL == "GPL1nnn"){
                return $scope.GPL2nnnannot= true;
            }
            else if($scope.select.GPL == "GPL2nnn"){
                return $scope.GPL2nnnannot= true;
            }
            else if($scope.select.GPL == "GPL3nnn"){
                return $scope.GPL3nnnannot= true;
            }
            else if($scope.select.GPL == "GPL4nnn"){
                return $scope.GPL4nnnannot= true;
            }
            else if($scope.select.GPL == "GPL5nnn"){
                return $scope.GPL5nnnannot= true;
            }
            else if($scope.select.GPL == "GPL6nnn"){
                return $scope.GPL6nnnannot= true;
            }
            else if($scope.select.GPL == "GPL7nnn"){
                return $scope.GPL7nnnannot= true;
            }
            else if($scope.select.GPL == "GPL8nnn"){
                return $scope.GPL8nnnannot= true;
            }
            else if($scope.select.GPL == "GPL9nnn"){
                return $scope.GPL9nnnannot= true;
            }
            else if($scope.select.GPL == "GPL10nnn"){
                return $scope.GPL10nnnannot= true;
            }
            else if($scope.select.GPL == "GPL11nnn"){
                return $scope.GPL11nnnannot= true;
            }
            else if($scope.select.GPL == "GPL12nnn"){
                return $scope.GPL12nnnannot= true;
            }
            else if($scope.select.GPL == "GPL13nnn"){
                return $scope.GPL13nnnannot= true;
            }
            else if($scope.select.GPL == "GPL14nnn"){
                return $scope.GPL14nnnannot= true;
            }
            
        }
        $scope.user = Auth.getUser();

        $scope.msg = "Dashboard Tools";
        $scope.listID = [];
        $scope.result="";
        $scope.species=0;
        $scope.way = ""

        $scope.user = null
        $scope.user = Auth.getUser();

        if($window.sessionStorage.token) {
            $scope.token = $window.sessionStorage.token;
        }

        // $scope.signatures = [];
        // $scope.selected = ""

        // if($scope.user == undefined || $scope.user == null){
        //   $scope.selected = $cookieStore.get('selectedID').split(',');
        // }
        // else{
        //   $scope.selected = $scope.user.selectedID.split(',');
        //   console.log($scope.selected);
        // }
        // console.log($scope.selected);
        // for(var i=0;i<$scope.selected.length;i++){
        //   console.log($scope.selected[i]);
        //   console.log(i);
        //   Dataset.get({'filter':$scope.selected[i],'from':'None','to': 'None','collection':'signatures','field':'id'}).$promise.then(function(data){
        //     $scope.signatures.push(data.request);
        //     console.log($scope.signatures);
        //   });
        // }


        // $scope.deleted = function(signature_id){
        //   // if($scope.user == undefined || $scope.user == null){
        //   //   $scope.selected = $cookieStore.get('selectedID').split(',');
        //   //   var index = $scope.selected.indexOf(signature_id);
        //   //   $scope.selected.splice(index, 1);
        //   //   var newcookie = $scope.selected.join(',');
        //   //   console.log(newcookie);
        //   //   $cookieStore.put('selectedID', newcookie);
        //   // }
        //   else{
        //     $scope.selected = $scope.user.selectedID.split(',');fredirect
        //     console.log($scope.selected);
        //     var index = $scope.selected.indexOf(signature_id);
        //     $scope.selected.splice(index, 1);
        //     $scope.user.selectedID = $scope.selected.join(',');
        //     $scope.user.$save({'uid': $scope.user.id}).then(function(data){
        //         $scope.user = data;
        //     });
        //   }
        // }

        $scope.toggleSelection2 = function toggleSelection2(genes) {
            $scope.listID = genes.split(',').join('\n');

        }


        $scope.convert = function(data){
          $scope.listID = $scope.listID.split('\n').join(',');
          console.log($scope.listID);
          Dataset.convert({'genes':$scope.listID,'way':$scope.way,'species':$scope.species}).$promise.then(function(data){
            $scope.convertedList = data.converted_list;
            $scope.result = data.converted_list;
          });
        };
});

app.controller('jobsCtrl',
    function ($scope,$rootScope, $log, Auth, User,$window, $cookieStore, Dataset, $location, ngDialog) {
        $scope.user = null
        $scope.user = Auth.getUser();


        if($window.sessionStorage.token) {
            $scope.token = $window.sessionStorage.token;
        }

        //console.log($scope.user);

        $scope.jobRunning = [];
        $scope.selected = ""

        if($scope.user == undefined || $scope.user == null){
          $scope.jobRunning = $cookieStore.get('jobID').split(',');
        }
        else{
          $scope.jobRunning = $scope.user.jobID.split(',');
          console.log($scope.jobRunning);
        }

        Dataset.getjob({'job_list':$scope.jobRunning}).$promise.then(function(data){
          $scope.jobs = data.jobs;
        });

        $scope.show_info = function(job){
          ngDialog.open({ template: 'lofInfo', scope: $scope, className: 'ngdialog-theme-default',data: job});
        }
        



        $scope.convert_timestamp_to_date = function(UNIX_timestamp){
          if(UNIX_timestamp=='' || UNIX_timestamp===null || UNIX_timestamp===undefined) { return '';}
          var a = new Date(UNIX_timestamp*1000);
          var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
          var year = a.getFullYear();
          var month = months[a.getMonth()];
          var date = a.getDate();
          var hour = a.getHours();
          var min = a.getMinutes();
          var sec = a.getSeconds();
          var time = date + ',' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
          return time;
        };

      $scope.show_result = function(job){
        var oid = job._id;
        console.log(oid['$oid']);
        $location.url('/jobresults?job='+oid['$oid']);

      }

      $scope.del_job = function(job){
        if($scope.user == undefined || $scope.user == null){
          var index = $scope.jobRunning.indexOf(job.id)
          if (index != -1){
            $scope.jobRunning.splice(index, 1);
            $cookieStore.put('jobID',$scope.jobRunning.join(','));
            $scope.jobRunning = $cookieStore.get('jobID').split(',');
            Dataset.getjob({'job_list':$scope.jobRunning}).$promise.then(function(data){
                $scope.jobs = data.jobs;
              });
          }
        }
        else{
          var index = $scope.jobRunning.indexOf(job.id.toString());
          if (index != -1){
            $scope.jobRunning.splice(index, 1);
            $scope.user.jobID = $scope.jobRunning.join(',');
            $scope.user.$save({'uid': $scope.user.id}).then(function(data){
              $scope.user = data;
              $scope.jobRunning = $scope.user.jobID.split(',');
               Dataset.getjob({'job_list':$scope.jobRunning}).$promise.then(function(data){
                $scope.jobs = data.jobs;
              });
            });
          }
        }
      }

});



app.controller('loginCtrl',
    function ($scope, $rootScope, $routeParams, $log, $location, $window, User, Auth, $cookieStore) {
        $scope.msg = null;

      var params = $location.search();

      if(params['action'] !== undefined && params['action'] == 'confirm_email') {
          User.confirm_email({}, {'token': params['token']}).$promise.then(function(data){
            $scope.msg=data['msg'];
                                if(data['status'] == 'danger'){
                                  $scope.danger=data['msg'];
                                }
                                else if(data['status'] == 'success'){
                                  $scope.success=data['msg'];
                                }
                                else if(data['status'] == 'warning'){
                                  $scope.warning=data['msg'];
                                }
          });
      }
      else if(params['token'] !== undefined) {
          User.is_authenticated({},{'token': params['token']}).$promise.then(function(data){
              $rootScope.$broadcast('loginCtrl.login', data);
              Auth.setUser(data);
              $window.sessionStorage.token = params['token'];
              $location.search('token', null);
              $location.path('');
          });
      }

      $scope.remember = function(){
        $cookieStore.put('remember','1');
      }


      
      $scope.login = function(user) {

          User.login({},{'user_name': user.mail, 'user_password': user.password}).$promise.then(function(data){
              
              if(data['status'] == 'danger'){
                $scope.danger='Contact the administrator';
              }
              else if(data['status'] == 'success'){
                User.is_authenticated({},{'token': data['token']}).$promise.then(function(data){
                     $rootScope.$broadcast('loginCtrl.login', data);
                     Auth.setUser(data);
                     $window.sessionStorage.token = data.token;
                     $location.search('token', null);
                     $location.path('');
                 });
              }
              else if(data['status'] == 'warning'){
              $scope.warning=data['msg'];
              }
          });
    };
    $scope.loginDemo = function() {
          User.login({},{'user_name': 'geneulike@gmail.com', 'user_password':'0000'}).$promise.then(function(data){
              if(data['status'] == 'danger'){
                $scope.danger='Contact the administrator';
              }
              else if(data['status'] == 'success'){
                User.is_authenticated({},{'token': data['token']}).$promise.then(function(data){
                     $rootScope.$broadcast('loginCtrl.login', data);
                     Auth.setUser(data);
                     $window.sessionStorage.token = data.token;
                     $location.search('token', null);
                     $location.path('');
                 });
              }
              else if(data['status'] == 'warning'){
              $scope.warning=data['msg'];
              }
          });
    };


});

app.controller('signinCtrl',
    function ($scope,$rootScope, $log, Auth, User,$location) {
            $scope.danger = null;
            $scope.warning = null;
            
            $scope.success = null;

            $scope.register = function(newUser){
            ////console.log("REGISTER");
              //console.log(newUser);

              // if (newUser.trim()==''){
              //   return $scope.warning = "Fill in the Registration Form before registering";
              // }
              // if( (newUser.firstname === undefined || newUser.firstname == '') && (newUser.lastname === undefined || newUser.lastname == '') && (newUser.email === undefined || newUser.email == '') ) {
              //   return $scope.warning = "Fill in the Registration Form before registering";
              // }
              if(newUser.firstname === undefined || newUser.firstname == ''){
                return $scope.warning = 'User first name is empty';
              }
              else if(newUser.lastname === undefined || newUser.lastname == ''){
                return $scope.warning = 'User last name is empty';
              }
              else if(newUser.email === undefined || newUser.email == ''){
                return $scope.warning = 'User email is empty and must be a valid email address';
              }
              else if(newUser.check_password === undefined || newUser.check_password == '' || newUser.check_password != newUser.password){
                return $scope.warning = 'Passwords do not match';
              }
              else {
                var laboratory = newUser.laboratory
                if(newUser.laboratory === undefined || newUser.laboratory == ''){
                  laboratory=null;
                }
                var country=newUser.country
                if(newUser.country === undefined || newUser.country == ''){
                  country=null;
                }
                  User.register({},{'user_name': newUser.email,
                                      'user_password':newUser.password,
                                      'first_name': newUser.firstname,
                                      'last_name': newUser.lastname,
                                      'country':country,
                                      'laboratory': laboratory,
                                  }).$promise.then(function(data){
                                    if(data['status'] == 'danger'){
                                      $scope.danger=data['msg'];
                                    }
                                    else if(data['status'] == 'success'){
                                      $scope.success=data['msg'];
                                    }
                                    else if(data['status'] == 'warning'){
                                      $scope.warning=data['msg'];
                                    }

                });
              }
          };

});




app.controller('recoverCtrl',
  function($scope, User, $log, $routeParams, $location){
        
        

        $scope.recover= function(userRecover){

          if(userRecover.mail === undefined || userRecover.mail == null){
            return $scope.warning= 'User mail field is empty.'
          }
          else{
            User.recover({},{'user_name': userRecover.mail}).$promise.then(function(data){
              if(data['status'] == 'danger'){
                $scope.danger=data['msg'];
              }
              else if(data['status'] == 'success'){
                $scope.success = data['msg'];
              }
              else if(data['status'] == 'warning'){
                $scope.warning=data['msg'];
              }
            });
          }

    };
  });

app.controller('passwordRecoverCtrl', 
  function($scope, User, $log, $location, $routeParams, $timeout){

    $scope.recover = function(passwordRecover){
      if(passwordRecover.password != passwordRecover.check_password){
        return $scope.warning = 'Passwords do not match';
      }
      else{
        var params = $location.search();
        User.confirm_recover({},{'token' : params['token'], 'user_password' : passwordRecover.password}).$promise.then(function(data){
              if(data['status'] == 'danger'){
                $scope.danger=data['msg'];
              }
              else if(data['status'] == 'success'){
                $scope.success = data['msg'];
                $timeout(function(){ 
                  $location.path('/login'); 
                  },1750);
              }
              else if(data['status'] == 'warning'){
                scope.warning=data['msg'];
              }
        });
      }
    };
});

app.controller('userInfoCtrl',
    function ($scope, $rootScope, $routeParams, $location, Auth, User) {
 
        User.get({'uid': $routeParams['id']}).$promise.then(function(data){
            $scope.user = data;
            $scope.joined=data['joined'].substr(0,10);

            

            });
        
        User.getLastSeen({},{'uid': $routeParams['id']}).$promise.then(function(data){
                 $scope.connected = "°" + data['connected'];
            });
        // User.getLastSeen({},{'data_joined': data['joined'] , 'data_connected' : data['connected']}).$promise.then(function(data){
        //          $scope.connected = data['connected'];
        //     });
            // var date = data['connected'];
            // var yearJoined = Number(data['joined'].substr(0,4));
            // if(Number(data['joined'].substr(0,4)) < Number(data['connected'].substr(0,4)) && Number(data['connected'].substr(0,4)) - Number(data['joined'].substr(0,4)) == 1){
            //     $scope.connected = "1 year ago";
            // }
            // else if(yearJoined  < Number(data['connected'].substr(0,4)) && Number(data['connected'].substr(0,4)) - yearJoined  != 1){
            //     $scope.connected=(Number(data['connected'].substr(0,4)) - yearJoined ).toString() + " years ago";
            // }
            // else if(Number(data['joined'].substr(5,7)) < Number(data['connected'].substr(5,7)) && Number(data['connected'].substr(5,7)) - Number(data['joined'].substr(5,7)) == 1){
            //     $scope.connected = "1 month ago";
            // }
            // else if(Number(data['joined'].substr(5,7)) < Number(data['connected'].substr(5,7)) && Number(data['connected'].substr(5,7)) - Number(data['joined'].substr(5,7)) != 1){
            //     $scope.connected=(Number(data['connected'].substr(5,7)) - Number(data['joined'].substr(5,7))).toString() + " months ago";
            // }
            // else if(Number(data['joined'].substr(8,10)) < Number(data['connected'].substr(8,10)) && Number(data['connected'].substr(8,10)) - Number(data['joined'].substr(8,10)) == 1){
            //     $scope.connected = "1 day ago";
            // }
            // else if(Number(data['joined'].substr(8,10)) < Number(data['connected'].substr(8,10)) && Number(data['connected'].substr(8,10)) - Number(data['joined'].substr(8,10)) != 1){
            //     $scope.connected=(Number(data['connected'].substr(8,10)) - Number(data['joined'].substr(8,10))).toString() + " days ago";
            // }
            // else if(Number(data['joined'].substr(11,13)) < Number(data['connected'].substr(11,13)) && Number(data['connected'].substr(11,13)) - Number(data['joined'].substr(11,13)) == 1){
            //     $scope.connected = "1 hour ago";
            // }
            // else if(Number(data['joined'].substr(11,13)) < Number(data['connected'].substr(11,13)) && Number(data['connected'].substr(11,13)) - Number(data['joined'].substr(11,13)) != 1){
            //     $scope.connected=(Number(data['connected'].substr(11,13)) - Number(data['joined'].substr(11,13))).toString() + " hours ago";
            // }
            // else if(Number(data['joined'].substr(14,16)) < Number(data['connected'].substr(14,16)) && Number(data['connected'].substr(14,16)) - Number(data['joined'].substr(14,16)) == 1){
            //     $scope.connected = "1 minute ago";
            // }
            // else if(Number(data['joined'].substr(14,16)) < Number(data['connected'].substr(14,16)) && Number(data['connected'].substr(14,16)) - Number(data['joined'].substr(14,16)) != 1){
            //     $scope.connected=(Number(data['connected'].substr(14,16)) - Number(data['joined'].substr(14,16))).toString() + " minutes ago";
            // }
            // else if(Number(data['joined'].substr(17,19)) < Number(data['connected'].substr(17,19)) && Number(data['connected'].substr(17,19)) - Number(data['joined'].substr(17,19)) == 1){
            //     $scope.connected = "1 second ago";
            // }
            // else{
            //     $scope.connected=(Number(data['connected'].substr(17,19)) - Number(data['joined'].substr(17,19))).toString() + " seconds ago";
            // }



        $scope.update = function() {
            if($scope.user != null) {
                                    //$scope?user?id
                $scope.user.$save({'uid': $routeParams['id']}).then(function(data){
                    console.log(data);
                    $scope.user = data;
                });
            }
        }
      $scope.auth_user = Auth.getUser();

});

app.controller('userprojectCtrl',
    function ($scope, $rootScope, $routeParams, $location, Auth,Dataset, User) {
        $scope.user = null;
        $scope.pfrom = 0;
        $scope.pto = 25;
        $scope.sfrom = 0;
        $scope.sto = 25;
        $scope.afrom = 0;
        $scope.ato = 25;
        $scope.sgfrom = 0;
        $scope.sgto = 25;

        User.get({'uid': $routeParams['id']}).$promise.then(function(data){
          
          $scope.user = data;

          Dataset.get({'filter':$scope.user.id,'from':$scope.pfrom,'to': $scope.pto,'collection':'projects','field':'owner','all_info':'true'}).$promise.then(function(data){
            $scope.projects = data.request;
            $scope.project_number = data.project_number;
            $scope.study_number = data.study_number;
            $scope.strategy_number = data.strategy_number;
            $scope.list_number = data.list_number;
          });
        });
      $scope.auth_user = Auth.getUser();

      

      $scope.test = "";

      $scope.showStudies = function(){
        Dataset.get({'filter':$scope.user.id,'from':$scope.sfrom,'to': $scope.sto,'collection':'studies','field':'owner'}).$promise.then(function(data){
            $scope.studies = data.request;
          });
      };

      $scope.showStrategies = function(){
        Dataset.get({'filter':$scope.user.id,'from':$scope.afrom,'to': $scope.ato,'collection':'strategies','field':'owner'}).$promise.then(function(data){
            $scope.strategies = data.request;
          });
      };

      $scope.showLists = function(){
        Dataset.get({'filter':$scope.user.id,'from':$scope.sgfrom,'to': $scope.sgto,'collection':'lists','field':'owner'}).$promise.then(function(data){
            $scope.lists = data.request;
          });
      };

      $scope.more = function(type){
        if(type=="projects"){
          console.log($scope.pfrom)
          console.log($scope.pto)
          $scope.pfrom = $scope.pto + 0;
          $scope.pto = $scope.pto + 25;
          console.log($scope.pfrom)
          console.log($scope.pto)
          Dataset.get({'filter':$scope.user.id,'from':$scope.pfrom,'to': $scope.pto,'collection':'projects','field':'owner'}).$promise.then(function(data){
            $scope.projects = data.request;
            console.log($scope.projects)
          });
        };
        if(type=="studies"){
          $scope.sfrom = $scope.sto + 0;
          $scope.sto = $scope.sto + 25;
          Dataset.get({'filter':$scope.user.id,'from':$scope.sfrom,'to': $scope.sto,'collection':'studies','field':'owner'}).$promise.then(function(data){
            $scope.studies = data.request;
          });
        };
        if(type=="strategies"){
          $scope.afrom = $scope.ato + 0;
          $scope.ato = $scope.ato + 25;
          Dataset.get({'filter':$scope.user.id,'from':$scope.afrom,'to': $scope.ato,'collection':'strategies','field':'owner'}).$promise.then(function(data){
            $scope.strategies = data.request;
          });
        };
        if(type=="lists"){
          $scope.sgfrom = $scope.sgto + 0;
          $scope.sgto = $scope.sgto + 25;
          Dataset.get({'filter':$scope.user.id,'from':$scope.sgfrom,'to': $scope.sgto,'collection':'lists','field':'owner'}).$promise.then(function(data){
            $scope.lists = data.request;
          });
        };
      }
      $scope.back = function(type){

        if(type=="projects"){
          $scope.pfrom = $scope.pfrom - 25 ;
          $scope.pto = $scope.pto - 25;
          Dataset.get({'filter':$scope.user.id,'from':$scope.pfrom,'to': $scope.pto,'collection':'projects','field':'owner'}).$promise.then(function(data){
            $scope.projects = data.request;
          });
        };
        if(type=="studies"){
          $scope.sfrom = $scope.sfrom - 25 ;
          $scope.sto = $scope.sto - 25;
          Dataset.get({'filter':$scope.user.id,'from':$scope.sfrom,'to': $scope.sto,'collection':'studies','field':'owner'}).$promise.then(function(data){
            $scope.studies = data.request;
          });
        };
        if(type=="strategies"){
          $scope.afrom = $scope.afrom - 25;
          $scope.ato = $scope.ato - 25;
          Dataset.get({'filter':$scope.user.id,'from':$scope.afrom,'to': $scope.ato,'collection':'strategies','field':'owner'}).$promise.then(function(data){
            $scope.strategies = data.request;
          });
        };
        if(type=="lists"){
          $scope.sgfrom = $scope.sgfrom - 25;
          $scope.sgto = $scope.sgto - 25;
          Dataset.get({'filter':$scope.user.id,'from':$scope.sgfrom,'to': $scope.sgto,'collection':'lists','field':'owner'}).$promise.then(function(data){
            $scope.lists = data.request;
          });
        };

      }



});

app.controller('compareCtrl',
    function ($scope,$rootScope, $log, Auth, User, Dataset,$cookies, $window, $cookieStore, ngDialog, $location) {
        $scope.msg = "Dashboard Tools";

        $scope.open_info = function(id){
          ngDialog.open({ template: id, className: 'ngdialog-theme-default'});
        }
        $scope.user = null
        $scope.user = Auth.getUser();

        if($window.sessionStorage.token) {
            $scope.token = $window.sessionStorage.token;
        }

        $scope.signatures = [];
        $scope.selected = ""

        if($scope.user == undefined || $scope.user == null){
          $scope.selected = $cookieStore.get('selectedID').split(',');
        }
        else{
          $scope.selected = $scope.user.selectedID.split(',');
          console.log($scope.selected);
        }
        console.log($scope.selected);
        for(var i=0;i<$scope.selected.length;i++){
          console.log($scope.selected[i]);
          console.log(i);
          Dataset.get({'filter':$scope.selected[i],'from':'None','to': 'None','collection':'signatures','field':'id'}).$promise.then(function(data){
            $scope.signatures.push(data.request);
            console.log($scope.signatures);
          });
        }


        $scope.deleted = function(signature_id){
          if($scope.user == undefined || $scope.user == null){
            $scope.selected = $cookieStore.get('selectedID').split(',');
            var index = $scope.selected.indexOf(signature_id);
            $scope.selected.splice(index, 1);
            var newcookie = $scope.selected.join(',');
            console.log(newcookie);
            $cookieStore.put('selectedID', newcookie);
          }
          else{
            $scope.selected = $scope.user.selectedID.split(',');
            console.log($scope.selected);
            var index = $scope.selected.indexOf(signature_id);
            $scope.selected.splice(index, 1);
            $scope.user.selectedID = $scope.selected.join(',');
            $scope.user.$save({'uid': $scope.user.id}).then(function(data){
                $scope.user = data;
            });
          }
        }

        

        $scope.selection = [];
        $scope.posistion = 0
        $scope.list = [{'list':1,'val':" "},{'list':2,'val':" "},{'list':3,'val':" "},{'list':4,'val':" "},{'list':5,'val':" "},{'list':6,'val':" "}]
        
        $scope.toggleSelection2 = function toggleSelection2(names,genes,id) {
          Dataset.convert({'genes':genes,'id':id,'way':'None'}).$promise.then(function(data){
            $scope.convertedList = data.converted_list;
            var name = "";
              name = id+'-'+names;

              var obj = name
              var idx = $scope.selection.indexOf(name);


              // is currently selected
              if (idx > -1) {
                $scope.selection.splice(idx, 1);
                for(var z=0;z<$scope.list.length;z++){
                  if($scope.list[z].val ==name){
                    $scope.list[z].val = " ";
                    document.getElementById('name'+$scope.list[z].list).value = "List"+$scope.list[z].list;
                    document.getElementById('area'+$scope.list[z].list).value = "";
                    break
                  }
                } 
              }

              // is newly selected
              else {
                $scope.selection.push(name);
                for(var z=0;z<$scope.list.length;z++){
                  if($scope.list[z].val ==" "){
                    $scope.list[z].val = name;
                    document.getElementById('name'+$scope.list[z].list).value = name;
                    document.getElementById('area'+$scope.list[z].list).value = $scope.convertedList.join('\n');
                    break
                  }
                } 
              }
          });
        }
});

//https://github.com/handsontable/handsontable/issues/2675
//http://techqa.info/programming/tag/handsontable?after=41589506
app.controller('createCtrl',
    function ($scope, $rootScope, $routeParams, $location, Auth, Dataset, User, Upload, ngDialog, $timeout, $http, $window) {

    $scope.$watch('$viewContentLoaded', function() {
        $timeout( function(){

            $scope.user = null;
            $scope.hasData=false;
            var data_projects=null;
            var data_strategies=null;
            var data_lists=null;
            var data1 = [],
                        container = document.getElementById('excelTable'),
                        settings = {
                            data: data1,
                            width: 1100,
                            height: 320,
                        },
                        hot1;
            hot1 = new Handsontable(container, settings);
            hot1.render();
            var whichTableView="project";
            $scope.ontologyDatabaseArray=[];
            $scope.ontoDatabaseSelected={};;
            $scope.warning="";
            $scope.success="";
            $scope.search_result=[];
            var row;
            var col;
            $scope.value;
            $scope.onto=null;
            $scope.viewOntology = true;
            $scope.stepProgressBar_UploadData = ""; // -1 : none, 0 : first step , 1 : second step, 2: third step , 3: fourth step
            $scope.stepProgressBar_CheckData = "";
            $scope.stepProgressBar_UploadLists = "";
            $scope.stepProgressBar_CheckLists = "";
            $scope.showExcelTable=true;
            $scope.report=false;
            $scope.message="";
            $scope.uploadList=true;
            $scope.objectFiles;
            $scope.canSubmit= {boolean : false};

            $scope.DBDatabaseArray = [
                {id : "Entrez"              , name : "Entrez Gene"},
                {id : "Ensembl_Gene"        , name : "Ensembl Gene"},
                {id : "Ensembl_protein"     , name : "Ensembl protein"},
                {id : "Ensembl_transcript"  , name : "Ensembl transcript"},
                {id : "GI_protein"          , name : "GI protein"},
                {id : "GI_transcript"       , name : "GI transcript"},
                {id : "GPL"                 , name : "GPL"},
                {id : "GenBank_protein"     , name : "GenBank protein"},
                {id : "GenBank_transcript"  , name : "GenBank transcript"},
                {id : "RefSeq_protein"      , name : "RefSeq protein"},
                {id : "RefSeq_transcript"   , name : "RefSeq transcript"},
                {id : "UniGene"             , name : "UniGene"},
                {id : "UniProt"             , name : "UniProt"},
                {id : "Vega_gene"           , name : "Vega gene"},
                {id : "Vega_protein"        , name : "Vega protein"},
                {id : "Vega_transcript"     , name : "Vega transcript"},
            ];
            $scope.DBDatabaseSelected = { value : "" };

            $scope.removeDBDatabaseSelected = function() {
                $scope.DBDatabaseSelected.value = "";
            };

            $scope.GPLVersionArray = [
                {id : "GPLnnn"      , name : "GPLnnn"},
                {id : "GPL1nnn"     , name : "GPL1nnn"},
                {id : "GPL2nnn"     , name : "GPL2nnn"},
                {id : "GPL3nnn"     , name : "GPL3nnn"},
                {id : "GPL4nnn"     , name : "GPL4nnn"},
                {id : "GPL5nnn"     , name : "GPL5nnn"},
                {id : "GPL6nnn"     , name : "GPL6nnn"},
                {id : "GPL7nnn"     , name : "GPL7nnn"},
                {id : "GPL8nnn"     , name : "GPL8nnn"},
                {id : "GPL9nnn"     , name : "GPL9nnn"},
                {id : "GPL10nnn"    , name : "GPL10nnn"},
                {id : "GPL11nnn"    , name : "GPL11nnn"},
                {id : "GPL12nnn"    , name : "GPL12nnn"},
                {id : "GPL13nnn"    , name : "GPL13nnn"},
                {id : "GPL14nnn"    , name : "GPL14nnn"},
                {id : "GPL15nnn"    , name : "GPL15nnn"},
                {id : "GPL16nnn"    , name : "GPL16nnn"},
                {id : "GPL17nnn"    , name : "GPL17nnn"},
                {id : "GPL18nnn"    , name : "GPL18nnn"},
                {id : "GPL19nnn"    , name : "GPL19nnn"},
                {id : "GPL20nnn"    , name : "GPL20nnn"},
                {id : "GPL21nnn"    , name : "GPL21nnn"},
                {id : "GPL22nnn"    , name : "GPL22nnn"},
                {id : "GPL23nnn"    , name : "GPL23nnn"},
 
            ];
            $scope.GPLVersionSelected = { value : "" };

            $scope.removeGPLVersionSelected = function() {
                $scope.GPLVersionSelected.value = "";
            };

            $scope.GPLNumberSelected = {value : ""};
            $scope.database=null;
            $scope.hasError={boolean : true};

            User.get({'uid': $routeParams['id']}).$promise.then(function(data){
                $scope.user = data;
            });

            $scope.auth_user = Auth.getUser();

            $scope.signature_upload = function(excel_file) {
                var resultInfo={'error':"",'critical':""};
                Upload.upload({
                    url: '/upload/'+$scope.user.id+'/excelupload',
                    fields: {'uid': $scope.user.id, 'dataset': 'tmp'},
                    file: excel_file
                }).progress(function (evt) {

                }).success(function (data, status, headers, config) {
                    data_projects = data['projects'];
                    data_strategies = data['strategies'];
                    data_lists = data['lists'];
                    $scope.hasData=true;
                    $scope.stepProgressBar_UploadData = "active";
                    if(whichTableView=="project"){//$scope.projectview){
                        table_project();
                        setOntologyProject ()
                    }         
                    else if(whichTableView=="strategy"){//$scope.strategyview){
                        table_strategy();
                        setOntologyStrategy();
                    }
                    else{
                        table_list();
                        setOntologyList();
                    }

                }).error(function (data, status, headers, config) {
                })
            
            };

            $scope.showProjects = function(){
                $scope.showExcelTable=true;
                whichTableView="project";
                table_project();
                setOntologyProject();
            };

            $scope.showStrategies = function(){
                $scope.showExcelTable=true;
                whichTableView="strategy";
                table_strategy();
                setOntologyStrategy();      
            };

            $scope.showLists = function(){
                $scope.showExcelTable=true;
                whichTableView="list";
                table_list();
                setOntologyList();     
            };

            function setOntologyProject (){
                $scope.ontologyDatabaseArray = [
                    {id : "NCBITAXON", name : "NCBI Organismal Classification (NCBITAXON)"},
                    {id : "CHEBI"    , name : "Chemical Entities of Biological Interest (CHEBI)"},
                    {id : "FMA"      , name : "Foundational Model of Anatomy (FMA)"},
                    {id : "HP"       , name : "Human Phenotype Ontology (HP)"},
                    {id : "PATO"     , name : "Phenotypic Quality Ontology (PATO)"},
                    {id : "DOID"     , name : "Human Disease Ontology (DOID)"},
                    {id : "GO"       , name : "Gene Ontology (GO)"},
                    {id : "CL"       , name : "Cell Ontology (CL)"},
                    {id : "BTO"      , name : "BRENDA Tissue and Enzyme Source Ontology (BTO)"},
                    {id : "MP"       , name : "Mammalian Phenotype Ontology (MP)"},
                    {id : "OBI"      , name : "Ontology for Biomedical Investigations (OBI)"},
                ];
                $scope.ontoDatabaseSelected = { value : "" };
            };
            
            function setOntologyStrategy (){
                $scope.ontologyDatabaseArray = [
                    {id : "NCBITAXON", name : "NCBI Organismal Classification (NCBITAXON)"},
                    {id : "CHEBI"    , name : "Chemical Entities of Biological Interest (CHEBI)"},
                    {id : "FMA"      , name : "Foundational Model of Anatomy (FMA)"},
                ];
                $scope.ontoDatabaseSelected = { value : "" };
            };

            function setOntologyList(){
                $scope.ontologyDatabaseArray = [
                    {id : "NCBITAXON", name : "NCBI Organismal Classification (NCBITAXON)"},
                    {id : "CHEBI"    , name : "Chemical Entities of Biological Interest (CHEBI)"},
                ];
                $scope.ontoDatabaseSelected = { value : "" };
            };

            function table_project(){
                data1 = data_projects,
                container = document.getElementById('excelTable'),
                settings = {
                    data:data1,
                    width: 1100,
                    height: 320,
                    stretchH: 'all',
                    rowHeights: 30, 
                    colWidths: [350,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75], 
                    rowHeaders:true,
                    colHeaders:true,
                    maxRows:9,
                    maxCols:101,
                    wordWrap:false,
                    renderer: 'html',
                    fixedRowsTop: 0,
                    fixedColumnsLeft: 1,
                    manualRowResize : false,
                    manualColumnResize: true,
                    manualRowResize: true,
                    allowEmpty: true,
                    cells: function (row, col, prop) {
                        var cellProperties = {};

                        if (row === 0) {
                            cellProperties.readOnly = true; 
                            cellProperties.className = "htCenter htMiddle";
                        }

                        if (row === 1){
                            cellProperties.renderer = customDropdownRenderer;
                            cellProperties.editor = "chosen";
                            cellProperties.width = 150;
                            cellProperties.chosenOptions ={
                                multiple: false,
                                data: [{'id':'Root', 'label':'Root'},{'id': 'GUP1', 'label': 'GUP1'}, {'id': 'GUP2', 'label': 'GUP2'}, {'id': 'GUP3', 'label': 'GUP3'}, {'id': 'GUP4', 'label': 'GUP4'}, {'id': 'GUP5', 'label': 'GUP5'}, {'id': 'GUP6', 'label': 'GUP6'}, {'id': 'GUP7', 'label': 'GUP7'}, {'id': 'GUP8', 'label': 'GUP8'}, {'id': 'GUP9', 'label': 'GUP9'}, {'id': 'GUP10', 'label': 'GUP10'}, {'id': 'GUP11', 'label': 'GUP11'}, {'id': 'GUP12', 'label': 'GUP12'}, {'id': 'GUP13', 'label': 'GUP13'}, {'id': 'GUP14', 'label': 'GUP14'}, {'id': 'GUP15', 'label': 'GUP15'}, {'id': 'GUP16', 'label': 'GUP16'}, {'id': 'GUP17', 'label': 'GUP17'}, {'id': 'GUP18', 'label': 'GUP18'}, {'id': 'GUP19', 'label': 'GUP19'}, {'id': 'GUP20', 'label': 'GUP20'}, {'id': 'GUP21', 'label': 'GUP21'}, {'id': 'GUP22', 'label': 'GUP22'}, {'id': 'GUP23', 'label': 'GUP23'}, {'id': 'GUP24', 'label': 'GUP24'}, {'id': 'GUP25', 'label': 'GUP25'}, {'id': 'GUP26', 'label': 'GUP26'}, {'id': 'GUP27', 'label': 'GUP27'}, {'id': 'GUP28', 'label': 'GUP28'}, {'id': 'GUP29', 'label': 'GUP29'}, {'id': 'GUP30', 'label': 'GUP30'}, {'id': 'GUP31', 'label': 'GUP31'}, {'id': 'GUP32', 'label': 'GUP32'}, {'id': 'GUP33', 'label': 'GUP33'}, {'id': 'GUP34', 'label': 'GUP34'}, {'id': 'GUP35', 'label': 'GUP35'}, {'id': 'GUP36', 'label': 'GUP36'}, {'id': 'GUP37', 'label': 'GUP37'}, {'id': 'GUP38', 'label': 'GUP38'}, {'id': 'GUP39', 'label': 'GUP39'}, {'id': 'GUP40', 'label': 'GUP40'}, {'id': 'GUP41', 'label': 'GUP41'}, {'id': 'GUP42', 'label': 'GUP42'}, {'id': 'GUP43', 'label': 'GUP43'}, {'id': 'GUP44', 'label': 'GUP44'}, {'id': 'GUP45', 'label': 'GUP45'}, {'id': 'GUP46', 'label': 'GUP46'}, {'id': 'GUP47', 'label': 'GUP47'}, {'id': 'GUP48', 'label': 'GUP48'}, {'id': 'GUP49', 'label': 'GUP49'}, {'id': 'GUP50', 'label': 'GUP50'}, {'id': 'GUP51', 'label': 'GUP51'}, {'id': 'GUP52', 'label': 'GUP52'}, {'id': 'GUP53', 'label': 'GUP53'}, {'id': 'GUP54', 'label': 'GUP54'}, {'id': 'GUP55', 'label': 'GUP55'}, {'id': 'GUP56', 'label': 'GUP56'}, {'id': 'GUP57', 'label': 'GUP57'}, {'id': 'GUP58', 'label': 'GUP58'}, {'id': 'GUP59', 'label': 'GUP59'}, {'id': 'GUP60', 'label': 'GUP60'}, {'id': 'GUP61', 'label': 'GUP61'}, {'id': 'GUP62', 'label': 'GUP62'}, {'id': 'GUP63', 'label': 'GUP63'}, {'id': 'GUP64', 'label': 'GUP64'}, {'id': 'GUP65', 'label': 'GUP65'}, {'id': 'GUP66', 'label': 'GUP66'}, {'id': 'GUP67', 'label': 'GUP67'}, {'id': 'GUP68', 'label': 'GUP68'}, {'id': 'GUP69', 'label': 'GUP69'}, {'id': 'GUP70', 'label': 'GUP70'}, {'id': 'GUP71', 'label': 'GUP71'}, {'id': 'GUP72', 'label': 'GUP72'}, {'id': 'GUP73', 'label': 'GUP73'}, {'id': 'GUP74', 'label': 'GUP74'}, {'id': 'GUP75', 'label': 'GUP75'}, {'id': 'GUP76', 'label': 'GUP76'}, {'id': 'GUP77', 'label': 'GUP77'}, {'id': 'GUP78', 'label': 'GUP78'}, {'id': 'GUP79', 'label': 'GUP79'}, {'id': 'GUP80', 'label': 'GUP80'}, {'id': 'GUP81', 'label': 'GUP81'}, {'id': 'GUP82', 'label': 'GUP82'}, {'id': 'GUP83', 'label': 'GUP83'}, {'id': 'GUP84', 'label': 'GUP84'}, {'id': 'GUP85', 'label': 'GUP85'}, {'id': 'GUP86', 'label': 'GUP86'}, {'id': 'GUP87', 'label': 'GUP87'}, {'id': 'GUP88', 'label': 'GUP88'}, {'id': 'GUP89', 'label': 'GUP89'}, {'id': 'GUP90', 'label': 'GUP90'}, {'id': 'GUP91', 'label': 'GUP91'}, {'id': 'GUP92', 'label': 'GUP92'}, {'id': 'GUP93', 'label': 'GUP93'}, {'id': 'GUP94', 'label': 'GUP94'}, {'id': 'GUP95', 'label': 'GUP95'}, {'id': 'GUP96', 'label': 'GUP96'}, {'id': 'GUP97', 'label': 'GUP97'}, {'id': 'GUP98', 'label': 'GUP98'}, {'id': 'GUP99', 'label': 'GUP99'}, {'id': 'GUP100', 'label': 'GUP100'}]
                            };
                        }

                        if (col === 0) {
                            cellProperties.readOnly = true; // uses function directly
                            cellProperties.className = "htCenter htMiddle";
                        }

                        if(row === 5 && col !==0){
                            cellProperties.readOnly = true; 
                            cellProperties.renderer = rowOntologyRenderer;
                            //cellProperties.color = 'black';
                        }
                        
                        return cellProperties;
                    },
                    afterChange: function (changes, source) {

                        if (!changes) {
                            return;
                        }
                        
                        $timeout(function(){
                          $scope.hasError.boolean= true;
                        });

                        $.each(changes, function (index, element) {
                            data_projects[element[0]][element[1]] = element[3];
                            //element[4] value before changement
                        });
                    },
                    afterSelection: function (r, c, r2, c2) {
                        if(r == 5 && c !=0){
                            $scope.warning="";
                            $scope.success="";
                            row=r;
                            col=c;
                            $scope.onto=null;
                            Dataset.ontologies({},{'stringToDict': true, 'string':data_projects[row][col]}).$promise.then(function(data){
                                $scope.value=data[0];
                            });
                            openOntology();
                        }
                    },
                },

                hot1;
                hot1 = new Handsontable(container, settings);
                hot1.render();

            };  

            function table_strategy(){

                data1 = data_strategies,
                container = document.getElementById('excelTable'),
                settings = {
                    data:data1,
                    width: 1100,
                    height: 320,
                    stretchH: 'all',
                    rowHeights: 30, 
                    colWidths: [350,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75], 
                    rowHeaders:true,
                    colHeaders:true,
                    maxRows:9,
                    maxCols:201,
                    wordWrap:false,
                    renderer: 'html',
                    fixedRowsTop: 0,
                    fixedColumnsLeft: 1,
                    //autoRowSize:true,
                    manualRowResize : false,
                    manualColumnResize: true,
                    manualRowResize: true,
                    allowEmpty: true,
                    cells: function (row, col, prop) {
                        var cellProperties = {};

                        if (row === 0) {
                            cellProperties.readOnly = true; 
                            cellProperties.className = "htCenter htMiddle";
                        }

                        if (row === 1){
                            cellProperties.renderer = customDropdownRenderer;
                            cellProperties.editor = "chosen";
                            cellProperties.width = 150;
                            cellProperties.chosenOptions ={
                                multiple: false,
                                data: [{'id': 'GUP1', 'label': 'GUP1'}, {'id': 'GUP2', 'label': 'GUP2'}, {'id': 'GUP3', 'label': 'GUP3'}, {'id': 'GUP4', 'label': 'GUP4'}, {'id': 'GUP5', 'label': 'GUP5'}, {'id': 'GUP6', 'label': 'GUP6'}, {'id': 'GUP7', 'label': 'GUP7'}, {'id': 'GUP8', 'label': 'GUP8'}, {'id': 'GUP9', 'label': 'GUP9'}, {'id': 'GUP10', 'label': 'GUP10'}, {'id': 'GUP11', 'label': 'GUP11'}, {'id': 'GUP12', 'label': 'GUP12'}, {'id': 'GUP13', 'label': 'GUP13'}, {'id': 'GUP14', 'label': 'GUP14'}, {'id': 'GUP15', 'label': 'GUP15'}, {'id': 'GUP16', 'label': 'GUP16'}, {'id': 'GUP17', 'label': 'GUP17'}, {'id': 'GUP18', 'label': 'GUP18'}, {'id': 'GUP19', 'label': 'GUP19'}, {'id': 'GUP20', 'label': 'GUP20'}, {'id': 'GUP21', 'label': 'GUP21'}, {'id': 'GUP22', 'label': 'GUP22'}, {'id': 'GUP23', 'label': 'GUP23'}, {'id': 'GUP24', 'label': 'GUP24'}, {'id': 'GUP25', 'label': 'GUP25'}, {'id': 'GUP26', 'label': 'GUP26'}, {'id': 'GUP27', 'label': 'GUP27'}, {'id': 'GUP28', 'label': 'GUP28'}, {'id': 'GUP29', 'label': 'GUP29'}, {'id': 'GUP30', 'label': 'GUP30'}, {'id': 'GUP31', 'label': 'GUP31'}, {'id': 'GUP32', 'label': 'GUP32'}, {'id': 'GUP33', 'label': 'GUP33'}, {'id': 'GUP34', 'label': 'GUP34'}, {'id': 'GUP35', 'label': 'GUP35'}, {'id': 'GUP36', 'label': 'GUP36'}, {'id': 'GUP37', 'label': 'GUP37'}, {'id': 'GUP38', 'label': 'GUP38'}, {'id': 'GUP39', 'label': 'GUP39'}, {'id': 'GUP40', 'label': 'GUP40'}, {'id': 'GUP41', 'label': 'GUP41'}, {'id': 'GUP42', 'label': 'GUP42'}, {'id': 'GUP43', 'label': 'GUP43'}, {'id': 'GUP44', 'label': 'GUP44'}, {'id': 'GUP45', 'label': 'GUP45'}, {'id': 'GUP46', 'label': 'GUP46'}, {'id': 'GUP47', 'label': 'GUP47'}, {'id': 'GUP48', 'label': 'GUP48'}, {'id': 'GUP49', 'label': 'GUP49'}, {'id': 'GUP50', 'label': 'GUP50'}, {'id': 'GUP51', 'label': 'GUP51'}, {'id': 'GUP52', 'label': 'GUP52'}, {'id': 'GUP53', 'label': 'GUP53'}, {'id': 'GUP54', 'label': 'GUP54'}, {'id': 'GUP55', 'label': 'GUP55'}, {'id': 'GUP56', 'label': 'GUP56'}, {'id': 'GUP57', 'label': 'GUP57'}, {'id': 'GUP58', 'label': 'GUP58'}, {'id': 'GUP59', 'label': 'GUP59'}, {'id': 'GUP60', 'label': 'GUP60'}, {'id': 'GUP61', 'label': 'GUP61'}, {'id': 'GUP62', 'label': 'GUP62'}, {'id': 'GUP63', 'label': 'GUP63'}, {'id': 'GUP64', 'label': 'GUP64'}, {'id': 'GUP65', 'label': 'GUP65'}, {'id': 'GUP66', 'label': 'GUP66'}, {'id': 'GUP67', 'label': 'GUP67'}, {'id': 'GUP68', 'label': 'GUP68'}, {'id': 'GUP69', 'label': 'GUP69'}, {'id': 'GUP70', 'label': 'GUP70'}, {'id': 'GUP71', 'label': 'GUP71'}, {'id': 'GUP72', 'label': 'GUP72'}, {'id': 'GUP73', 'label': 'GUP73'}, {'id': 'GUP74', 'label': 'GUP74'}, {'id': 'GUP75', 'label': 'GUP75'}, {'id': 'GUP76', 'label': 'GUP76'}, {'id': 'GUP77', 'label': 'GUP77'}, {'id': 'GUP78', 'label': 'GUP78'}, {'id': 'GUP79', 'label': 'GUP79'}, {'id': 'GUP80', 'label': 'GUP80'}, {'id': 'GUP81', 'label': 'GUP81'}, {'id': 'GUP82', 'label': 'GUP82'}, {'id': 'GUP83', 'label': 'GUP83'}, {'id': 'GUP84', 'label': 'GUP84'}, {'id': 'GUP85', 'label': 'GUP85'}, {'id': 'GUP86', 'label': 'GUP86'}, {'id': 'GUP87', 'label': 'GUP87'}, {'id': 'GUP88', 'label': 'GUP88'}, {'id': 'GUP89', 'label': 'GUP89'}, {'id': 'GUP90', 'label': 'GUP90'}, {'id': 'GUP91', 'label': 'GUP91'}, {'id': 'GUP92', 'label': 'GUP92'}, {'id': 'GUP93', 'label': 'GUP93'}, {'id': 'GUP94', 'label': 'GUP94'}, {'id': 'GUP95', 'label': 'GUP95'}, {'id': 'GUP96', 'label': 'GUP96'}, {'id': 'GUP97', 'label': 'GUP97'}, {'id': 'GUP98', 'label': 'GUP98'}, {'id': 'GUP99', 'label': 'GUP99'}, {'id': 'GUP100', 'label': 'GUP100'}]
                            };
                        }

                        if (row === 2){
                            cellProperties.renderer = customDropdownRenderer;
                            cellProperties.editor = "chosen";
                            cellProperties.width = 500;
                            cellProperties.chosenOptions ={
                                multiple: true,
                                data: [{'id': 'Root', 'label': 'Root'},{'id': 'GUL1', 'label': 'GUL1'}, {'id': 'GUL2', 'label': 'GUL2'}, {'id': 'GUL3', 'label': 'GUL3'}, {'id': 'GUL4', 'label': 'GUL4'}, {'id': 'GUL5', 'label': 'GUL5'}, {'id': 'GUL6', 'label': 'GUL6'}, {'id': 'GUL7', 'label': 'GUL7'}, {'id': 'GUL8', 'label': 'GUL8'}, {'id': 'GUL9', 'label': 'GUL9'}, {'id': 'GUL10', 'label': 'GUL10'}, {'id': 'GUL11', 'label': 'GUL11'}, {'id': 'GUL12', 'label': 'GUL12'}, {'id': 'GUL13', 'label': 'GUL13'}, {'id': 'GUL14', 'label': 'GUL14'}, {'id': 'GUL15', 'label': 'GUL15'}, {'id': 'GUL16', 'label': 'GUL16'}, {'id': 'GUL17', 'label': 'GUL17'}, {'id': 'GUL18', 'label': 'GUL18'}, {'id': 'GUL19', 'label': 'GUL19'}, {'id': 'GUL20', 'label': 'GUL20'}, {'id': 'GUL21', 'label': 'GUL21'}, {'id': 'GUL22', 'label': 'GUL22'}, {'id': 'GUL23', 'label': 'GUL23'}, {'id': 'GUL24', 'label': 'GUL24'}, {'id': 'GUL25', 'label': 'GUL25'}, {'id': 'GUL26', 'label': 'GUL26'}, {'id': 'GUL27', 'label': 'GUL27'}, {'id': 'GUL28', 'label': 'GUL28'}, {'id': 'GUL29', 'label': 'GUL29'}, {'id': 'GUL30', 'label': 'GUL30'}, {'id': 'GUL31', 'label': 'GUL31'}, {'id': 'GUL32', 'label': 'GUL32'}, {'id': 'GUL33', 'label': 'GUL33'}, {'id': 'GUL34', 'label': 'GUL34'}, {'id': 'GUL35', 'label': 'GUL35'}, {'id': 'GUL36', 'label': 'GUL36'}, {'id': 'GUL37', 'label': 'GUL37'}, {'id': 'GUL38', 'label': 'GUL38'}, {'id': 'GUL39', 'label': 'GUL39'}, {'id': 'GUL40', 'label': 'GUL40'}, {'id': 'GUL41', 'label': 'GUL41'}, {'id': 'GUL42', 'label': 'GUL42'}, {'id': 'GUL43', 'label': 'GUL43'}, {'id': 'GUL44', 'label': 'GUL44'}, {'id': 'GUL45', 'label': 'GUL45'}, {'id': 'GUL46', 'label': 'GUL46'}, {'id': 'GUL47', 'label': 'GUL47'}, {'id': 'GUL48', 'label': 'GUL48'}, {'id': 'GUL49', 'label': 'GUL49'}, {'id': 'GUL50', 'label': 'GUL50'}, {'id': 'GUL51', 'label': 'GUL51'}, {'id': 'GUL52', 'label': 'GUL52'}, {'id': 'GUL53', 'label': 'GUL53'}, {'id': 'GUL54', 'label': 'GUL54'}, {'id': 'GUL55', 'label': 'GUL55'}, {'id': 'GUL56', 'label': 'GUL56'}, {'id': 'GUL57', 'label': 'GUL57'}, {'id': 'GUL58', 'label': 'GUL58'}, {'id': 'GUL59', 'label': 'GUL59'}, {'id': 'GUL60', 'label': 'GUL60'}, {'id': 'GUL61', 'label': 'GUL61'}, {'id': 'GUL62', 'label': 'GUL62'}, {'id': 'GUL63', 'label': 'GUL63'}, {'id': 'GUL64', 'label': 'GUL64'}, {'id': 'GUL65', 'label': 'GUL65'}, {'id': 'GUL66', 'label': 'GUL66'}, {'id': 'GUL67', 'label': 'GUL67'}, {'id': 'GUL68', 'label': 'GUL68'}, {'id': 'GUL69', 'label': 'GUL69'}, {'id': 'GUL70', 'label': 'GUL70'}, {'id': 'GUL71', 'label': 'GUL71'}, {'id': 'GUL72', 'label': 'GUL72'}, {'id': 'GUL73', 'label': 'GUL73'}, {'id': 'GUL74', 'label': 'GUL74'}, {'id': 'GUL75', 'label': 'GUL75'}, {'id': 'GUL76', 'label': 'GUL76'}, {'id': 'GUL77', 'label': 'GUL77'}, {'id': 'GUL78', 'label': 'GUL78'}, {'id': 'GUL79', 'label': 'GUL79'}, {'id': 'GUL80', 'label': 'GUL80'}, {'id': 'GUL81', 'label': 'GUL81'}, {'id': 'GUL82', 'label': 'GUL82'}, {'id': 'GUL83', 'label': 'GUL83'}, {'id': 'GUL84', 'label': 'GUL84'}, {'id': 'GUL85', 'label': 'GUL85'}, {'id': 'GUL86', 'label': 'GUL86'}, {'id': 'GUL87', 'label': 'GUL87'}, {'id': 'GUL88', 'label': 'GUL88'}, {'id': 'GUL89', 'label': 'GUL89'}, {'id': 'GUL90', 'label': 'GUL90'}, {'id': 'GUL91', 'label': 'GUL91'}, {'id': 'GUL92', 'label': 'GUL92'}, {'id': 'GUL93', 'label': 'GUL93'}, {'id': 'GUL94', 'label': 'GUL94'}, {'id': 'GUL95', 'label': 'GUL95'}, {'id': 'GUL96', 'label': 'GUL96'}, {'id': 'GUL97', 'label': 'GUL97'}, {'id': 'GUL98', 'label': 'GUL98'}, {'id': 'GUL99', 'label': 'GUL99'}, {'id': 'GUL100', 'label': 'GUL100'}, {'id': 'GUL101', 'label': 'GUL101'}, {'id': 'GUL102', 'label': 'GUL102'}, {'id': 'GUL103', 'label': 'GUL103'}, {'id': 'GUL104', 'label': 'GUL104'}, {'id': 'GUL105', 'label': 'GUL105'}, {'id': 'GUL106', 'label': 'GUL106'}, {'id': 'GUL107', 'label': 'GUL107'}, {'id': 'GUL108', 'label': 'GUL108'}, {'id': 'GUL109', 'label': 'GUL109'}, {'id': 'GUL110', 'label': 'GUL110'}, {'id': 'GUL111', 'label': 'GUL111'}, {'id': 'GUL112', 'label': 'GUL112'}, {'id': 'GUL113', 'label': 'GUL113'}, {'id': 'GUL114', 'label': 'GUL114'}, {'id': 'GUL115', 'label': 'GUL115'}, {'id': 'GUL116', 'label': 'GUL116'}, {'id': 'GUL117', 'label': 'GUL117'}, {'id': 'GUL118', 'label': 'GUL118'}, {'id': 'GUL119', 'label': 'GUL119'}, {'id': 'GUL120', 'label': 'GUL120'}, {'id': 'GUL121', 'label': 'GUL121'}, {'id': 'GUL122', 'label': 'GUL122'}, {'id': 'GUL123', 'label': 'GUL123'}, {'id': 'GUL124', 'label': 'GUL124'}, {'id': 'GUL125', 'label': 'GUL125'}, {'id': 'GUL126', 'label': 'GUL126'}, {'id': 'GUL127', 'label': 'GUL127'}, {'id': 'GUL128', 'label': 'GUL128'}, {'id': 'GUL129', 'label': 'GUL129'}, {'id': 'GUL130', 'label': 'GUL130'}, {'id': 'GUL131', 'label': 'GUL131'}, {'id': 'GUL132', 'label': 'GUL132'}, {'id': 'GUL133', 'label': 'GUL133'}, {'id': 'GUL134', 'label': 'GUL134'}, {'id': 'GUL135', 'label': 'GUL135'}, {'id': 'GUL136', 'label': 'GUL136'}, {'id': 'GUL137', 'label': 'GUL137'}, {'id': 'GUL138', 'label': 'GUL138'}, {'id': 'GUL139', 'label': 'GUL139'}, {'id': 'GUL140', 'label': 'GUL140'}, {'id': 'GUL141', 'label': 'GUL141'}, {'id': 'GUL142', 'label': 'GUL142'}, {'id': 'GUL143', 'label': 'GUL143'}, {'id': 'GUL144', 'label': 'GUL144'}, {'id': 'GUL145', 'label': 'GUL145'}, {'id': 'GUL146', 'label': 'GUL146'}, {'id': 'GUL147', 'label': 'GUL147'}, {'id': 'GUL148', 'label': 'GUL148'}, {'id': 'GUL149', 'label': 'GUL149'}, {'id': 'GUL150', 'label': 'GUL150'}, {'id': 'GUL151', 'label': 'GUL151'}, {'id': 'GUL152', 'label': 'GUL152'}, {'id': 'GUL153', 'label': 'GUL153'}, {'id': 'GUL154', 'label': 'GUL154'}, {'id': 'GUL155', 'label': 'GUL155'}, {'id': 'GUL156', 'label': 'GUL156'}, {'id': 'GUL157', 'label': 'GUL157'}, {'id': 'GUL158', 'label': 'GUL158'}, {'id': 'GUL159', 'label': 'GUL159'}, {'id': 'GUL160', 'label': 'GUL160'}, {'id': 'GUL161', 'label': 'GUL161'}, {'id': 'GUL162', 'label': 'GUL162'}, {'id': 'GUL163', 'label': 'GUL163'}, {'id': 'GUL164', 'label': 'GUL164'}, {'id': 'GUL165', 'label': 'GUL165'}, {'id': 'GUL166', 'label': 'GUL166'}, {'id': 'GUL167', 'label': 'GUL167'}, {'id': 'GUL168', 'label': 'GUL168'}, {'id': 'GUL169', 'label': 'GUL169'}, {'id': 'GUL170', 'label': 'GUL170'}, {'id': 'GUL171', 'label': 'GUL171'}, {'id': 'GUL172', 'label': 'GUL172'}, {'id': 'GUL173', 'label': 'GUL173'}, {'id': 'GUL174', 'label': 'GUL174'}, {'id': 'GUL175', 'label': 'GUL175'}, {'id': 'GUL176', 'label': 'GUL176'}, {'id': 'GUL177', 'label': 'GUL177'}, {'id': 'GUL178', 'label': 'GUL178'}, {'id': 'GUL179', 'label': 'GUL179'}, {'id': 'GUL180', 'label': 'GUL180'}, {'id': 'GUL181', 'label': 'GUL181'}, {'id': 'GUL182', 'label': 'GUL182'}, {'id': 'GUL183', 'label': 'GUL183'}, {'id': 'GUL184', 'label': 'GUL184'}, {'id': 'GUL185', 'label': 'GUL185'}, {'id': 'GUL186', 'label': 'GUL186'}, {'id': 'GUL187', 'label': 'GUL187'}, {'id': 'GUL188', 'label': 'GUL188'}, {'id': 'GUL189', 'label': 'GUL189'}, {'id': 'GUL190', 'label': 'GUL190'}, {'id': 'GUL191', 'label': 'GUL191'}, {'id': 'GUL192', 'label': 'GUL192'}, {'id': 'GUL193', 'label': 'GUL193'}, {'id': 'GUL194', 'label': 'GUL194'}, {'id': 'GUL195', 'label': 'GUL195'}, {'id': 'GUL196', 'label': 'GUL196'}, {'id': 'GUL197', 'label': 'GUL197'}, {'id': 'GUL198', 'label': 'GUL198'}, {'id': 'GUL199', 'label': 'GUL199'}, {'id': 'GUL200', 'label': 'GUL200'}, {'id': 'GUL201', 'label': 'GUL201'}, {'id': 'GUL202', 'label': 'GUL202'}, {'id': 'GUL203', 'label': 'GUL203'}, {'id': 'GUL204', 'label': 'GUL204'}, {'id': 'GUL205', 'label': 'GUL205'}, {'id': 'GUL206', 'label': 'GUL206'}, {'id': 'GUL207', 'label': 'GUL207'}, {'id': 'GUL208', 'label': 'GUL208'}, {'id': 'GUL209', 'label': 'GUL209'}, {'id': 'GUL210', 'label': 'GUL210'}, {'id': 'GUL211', 'label': 'GUL211'}, {'id': 'GUL212', 'label': 'GUL212'}, {'id': 'GUL213', 'label': 'GUL213'}, {'id': 'GUL214', 'label': 'GUL214'}, {'id': 'GUL215', 'label': 'GUL215'}, {'id': 'GUL216', 'label': 'GUL216'}, {'id': 'GUL217', 'label': 'GUL217'}, {'id': 'GUL218', 'label': 'GUL218'}, {'id': 'GUL219', 'label': 'GUL219'}, {'id': 'GUL220', 'label': 'GUL220'}, {'id': 'GUL221', 'label': 'GUL221'}, {'id': 'GUL222', 'label': 'GUL222'}, {'id': 'GUL223', 'label': 'GUL223'}, {'id': 'GUL224', 'label': 'GUL224'}, {'id': 'GUL225', 'label': 'GUL225'}, {'id': 'GUL226', 'label': 'GUL226'}, {'id': 'GUL227', 'label': 'GUL227'}, {'id': 'GUL228', 'label': 'GUL228'}, {'id': 'GUL229', 'label': 'GUL229'}, {'id': 'GUL230', 'label': 'GUL230'}, {'id': 'GUL231', 'label': 'GUL231'}, {'id': 'GUL232', 'label': 'GUL232'}, {'id': 'GUL233', 'label': 'GUL233'}, {'id': 'GUL234', 'label': 'GUL234'}, {'id': 'GUL235', 'label': 'GUL235'}, {'id': 'GUL236', 'label': 'GUL236'}, {'id': 'GUL237', 'label': 'GUL237'}, {'id': 'GUL238', 'label': 'GUL238'}, {'id': 'GUL239', 'label': 'GUL239'}, {'id': 'GUL240', 'label': 'GUL240'}, {'id': 'GUL241', 'label': 'GUL241'}, {'id': 'GUL242', 'label': 'GUL242'}, {'id': 'GUL243', 'label': 'GUL243'}, {'id': 'GUL244', 'label': 'GUL244'}, {'id': 'GUL245', 'label': 'GUL245'}, {'id': 'GUL246', 'label': 'GUL246'}, {'id': 'GUL247', 'label': 'GUL247'}, {'id': 'GUL248', 'label': 'GUL248'}, {'id': 'GUL249', 'label': 'GUL249'}, {'id': 'GUL250', 'label': 'GUL250'}, {'id': 'GUL251', 'label': 'GUL251'}, {'id': 'GUL252', 'label': 'GUL252'}, {'id': 'GUL253', 'label': 'GUL253'}, {'id': 'GUL254', 'label': 'GUL254'}, {'id': 'GUL255', 'label': 'GUL255'}, {'id': 'GUL256', 'label': 'GUL256'}, {'id': 'GUL257', 'label': 'GUL257'}, {'id': 'GUL258', 'label': 'GUL258'}, {'id': 'GUL259', 'label': 'GUL259'}, {'id': 'GUL260', 'label': 'GUL260'}, {'id': 'GUL261', 'label': 'GUL261'}, {'id': 'GUL262', 'label': 'GUL262'}, {'id': 'GUL263', 'label': 'GUL263'}, {'id': 'GUL264', 'label': 'GUL264'}, {'id': 'GUL265', 'label': 'GUL265'}, {'id': 'GUL266', 'label': 'GUL266'}, {'id': 'GUL267', 'label': 'GUL267'}, {'id': 'GUL268', 'label': 'GUL268'}, {'id': 'GUL269', 'label': 'GUL269'}, {'id': 'GUL270', 'label': 'GUL270'}, {'id': 'GUL271', 'label': 'GUL271'}, {'id': 'GUL272', 'label': 'GUL272'}, {'id': 'GUL273', 'label': 'GUL273'}, {'id': 'GUL274', 'label': 'GUL274'}, {'id': 'GUL275', 'label': 'GUL275'}, {'id': 'GUL276', 'label': 'GUL276'}, {'id': 'GUL277', 'label': 'GUL277'}, {'id': 'GUL278', 'label': 'GUL278'}, {'id': 'GUL279', 'label': 'GUL279'}, {'id': 'GUL280', 'label': 'GUL280'}, {'id': 'GUL281', 'label': 'GUL281'}, {'id': 'GUL282', 'label': 'GUL282'}, {'id': 'GUL283', 'label': 'GUL283'}, {'id': 'GUL284', 'label': 'GUL284'}, {'id': 'GUL285', 'label': 'GUL285'}, {'id': 'GUL286', 'label': 'GUL286'}, {'id': 'GUL287', 'label': 'GUL287'}, {'id': 'GUL288', 'label': 'GUL288'}, {'id': 'GUL289', 'label': 'GUL289'}, {'id': 'GUL290', 'label': 'GUL290'}, {'id': 'GUL291', 'label': 'GUL291'}, {'id': 'GUL292', 'label': 'GUL292'}, {'id': 'GUL293', 'label': 'GUL293'}, {'id': 'GUL294', 'label': 'GUL294'}, {'id': 'GUL295', 'label': 'GUL295'}, {'id': 'GUL296', 'label': 'GUL296'}, {'id': 'GUL297', 'label': 'GUL297'}, {'id': 'GUL298', 'label': 'GUL298'}, {'id': 'GUL299', 'label': 'GUL299'}, {'id': 'GUL300', 'label': 'GUL300'}, {'id': 'GUL301', 'label': 'GUL301'}, {'id': 'GUL302', 'label': 'GUL302'}, {'id': 'GUL303', 'label': 'GUL303'}, {'id': 'GUL304', 'label': 'GUL304'}, {'id': 'GUL305', 'label': 'GUL305'}, {'id': 'GUL306', 'label': 'GUL306'}, {'id': 'GUL307', 'label': 'GUL307'}, {'id': 'GUL308', 'label': 'GUL308'}, {'id': 'GUL309', 'label': 'GUL309'}, {'id': 'GUL310', 'label': 'GUL310'}, {'id': 'GUL311', 'label': 'GUL311'}, {'id': 'GUL312', 'label': 'GUL312'}, {'id': 'GUL313', 'label': 'GUL313'}, {'id': 'GUL314', 'label': 'GUL314'}, {'id': 'GUL315', 'label': 'GUL315'}, {'id': 'GUL316', 'label': 'GUL316'}, {'id': 'GUL317', 'label': 'GUL317'}, {'id': 'GUL318', 'label': 'GUL318'}, {'id': 'GUL319', 'label': 'GUL319'}, {'id': 'GUL320', 'label': 'GUL320'}, {'id': 'GUL321', 'label': 'GUL321'}, {'id': 'GUL322', 'label': 'GUL322'}, {'id': 'GUL323', 'label': 'GUL323'}, {'id': 'GUL324', 'label': 'GUL324'}, {'id': 'GUL325', 'label': 'GUL325'}, {'id': 'GUL326', 'label': 'GUL326'}, {'id': 'GUL327', 'label': 'GUL327'}, {'id': 'GUL328', 'label': 'GUL328'}, {'id': 'GUL329', 'label': 'GUL329'}, {'id': 'GUL330', 'label': 'GUL330'}, {'id': 'GUL331', 'label': 'GUL331'}, {'id': 'GUL332', 'label': 'GUL332'}, {'id': 'GUL333', 'label': 'GUL333'}, {'id': 'GUL334', 'label': 'GUL334'}, {'id': 'GUL335', 'label': 'GUL335'}, {'id': 'GUL336', 'label': 'GUL336'}, {'id': 'GUL337', 'label': 'GUL337'}, {'id': 'GUL338', 'label': 'GUL338'}, {'id': 'GUL339', 'label': 'GUL339'}, {'id': 'GUL340', 'label': 'GUL340'}, {'id': 'GUL341', 'label': 'GUL341'}, {'id': 'GUL342', 'label': 'GUL342'}, {'id': 'GUL343', 'label': 'GUL343'}, {'id': 'GUL344', 'label': 'GUL344'}, {'id': 'GUL345', 'label': 'GUL345'}, {'id': 'GUL346', 'label': 'GUL346'}, {'id': 'GUL347', 'label': 'GUL347'}, {'id': 'GUL348', 'label': 'GUL348'}, {'id': 'GUL349', 'label': 'GUL349'}, {'id': 'GUL350', 'label': 'GUL350'}, {'id': 'GUL351', 'label': 'GUL351'}, {'id': 'GUL352', 'label': 'GUL352'}, {'id': 'GUL353', 'label': 'GUL353'}, {'id': 'GUL354', 'label': 'GUL354'}, {'id': 'GUL355', 'label': 'GUL355'}, {'id': 'GUL356', 'label': 'GUL356'}, {'id': 'GUL357', 'label': 'GUL357'}, {'id': 'GUL358', 'label': 'GUL358'}, {'id': 'GUL359', 'label': 'GUL359'}, {'id': 'GUL360', 'label': 'GUL360'}, {'id': 'GUL361', 'label': 'GUL361'}, {'id': 'GUL362', 'label': 'GUL362'}, {'id': 'GUL363', 'label': 'GUL363'}, {'id': 'GUL364', 'label': 'GUL364'}, {'id': 'GUL365', 'label': 'GUL365'}, {'id': 'GUL366', 'label': 'GUL366'}, {'id': 'GUL367', 'label': 'GUL367'}, {'id': 'GUL368', 'label': 'GUL368'}, {'id': 'GUL369', 'label': 'GUL369'}, {'id': 'GUL370', 'label': 'GUL370'}, {'id': 'GUL371', 'label': 'GUL371'}, {'id': 'GUL372', 'label': 'GUL372'}, {'id': 'GUL373', 'label': 'GUL373'}, {'id': 'GUL374', 'label': 'GUL374'}, {'id': 'GUL375', 'label': 'GUL375'}, {'id': 'GUL376', 'label': 'GUL376'}, {'id': 'GUL377', 'label': 'GUL377'}, {'id': 'GUL378', 'label': 'GUL378'}, {'id': 'GUL379', 'label': 'GUL379'}, {'id': 'GUL380', 'label': 'GUL380'}, {'id': 'GUL381', 'label': 'GUL381'}, {'id': 'GUL382', 'label': 'GUL382'}, {'id': 'GUL383', 'label': 'GUL383'}, {'id': 'GUL384', 'label': 'GUL384'}, {'id': 'GUL385', 'label': 'GUL385'}, {'id': 'GUL386', 'label': 'GUL386'}, {'id': 'GUL387', 'label': 'GUL387'}, {'id': 'GUL388', 'label': 'GUL388'}, {'id': 'GUL389', 'label': 'GUL389'}, {'id': 'GUL390', 'label': 'GUL390'}, {'id': 'GUL391', 'label': 'GUL391'}, {'id': 'GUL392', 'label': 'GUL392'}, {'id': 'GUL393', 'label': 'GUL393'}, {'id': 'GUL394', 'label': 'GUL394'}, {'id': 'GUL395', 'label': 'GUL395'}, {'id': 'GUL396', 'label': 'GUL396'}, {'id': 'GUL397', 'label': 'GUL397'}, {'id': 'GUL398', 'label': 'GUL398'}, {'id': 'GUL399', 'label': 'GUL399'}, {'id': 'GUL400', 'label': 'GUL400'}, {'id': 'GUL401', 'label': 'GUL401'}, {'id': 'GUL402', 'label': 'GUL402'}, {'id': 'GUL403', 'label': 'GUL403'}, {'id': 'GUL404', 'label': 'GUL404'}, {'id': 'GUL405', 'label': 'GUL405'}, {'id': 'GUL406', 'label': 'GUL406'}, {'id': 'GUL407', 'label': 'GUL407'}, {'id': 'GUL408', 'label': 'GUL408'}, {'id': 'GUL409', 'label': 'GUL409'}, {'id': 'GUL410', 'label': 'GUL410'}, {'id': 'GUL411', 'label': 'GUL411'}, {'id': 'GUL412', 'label': 'GUL412'}, {'id': 'GUL413', 'label': 'GUL413'}, {'id': 'GUL414', 'label': 'GUL414'}, {'id': 'GUL415', 'label': 'GUL415'}, {'id': 'GUL416', 'label': 'GUL416'}, {'id': 'GUL417', 'label': 'GUL417'}, {'id': 'GUL418', 'label': 'GUL418'}, {'id': 'GUL419', 'label': 'GUL419'}, {'id': 'GUL420', 'label': 'GUL420'}, {'id': 'GUL421', 'label': 'GUL421'}, {'id': 'GUL422', 'label': 'GUL422'}, {'id': 'GUL423', 'label': 'GUL423'}, {'id': 'GUL424', 'label': 'GUL424'}, {'id': 'GUL425', 'label': 'GUL425'}, {'id': 'GUL426', 'label': 'GUL426'}, {'id': 'GUL427', 'label': 'GUL427'}, {'id': 'GUL428', 'label': 'GUL428'}, {'id': 'GUL429', 'label': 'GUL429'}, {'id': 'GUL430', 'label': 'GUL430'}, {'id': 'GUL431', 'label': 'GUL431'}, {'id': 'GUL432', 'label': 'GUL432'}, {'id': 'GUL433', 'label': 'GUL433'}, {'id': 'GUL434', 'label': 'GUL434'}, {'id': 'GUL435', 'label': 'GUL435'}, {'id': 'GUL436', 'label': 'GUL436'}, {'id': 'GUL437', 'label': 'GUL437'}, {'id': 'GUL438', 'label': 'GUL438'}, {'id': 'GUL439', 'label': 'GUL439'}, {'id': 'GUL440', 'label': 'GUL440'}, {'id': 'GUL441', 'label': 'GUL441'}, {'id': 'GUL442', 'label': 'GUL442'}, {'id': 'GUL443', 'label': 'GUL443'}, {'id': 'GUL444', 'label': 'GUL444'}, {'id': 'GUL445', 'label': 'GUL445'}, {'id': 'GUL446', 'label': 'GUL446'}, {'id': 'GUL447', 'label': 'GUL447'}, {'id': 'GUL448', 'label': 'GUL448'}, {'id': 'GUL449', 'label': 'GUL449'}, {'id': 'GUL450', 'label': 'GUL450'}, {'id': 'GUL451', 'label': 'GUL451'}, {'id': 'GUL452', 'label': 'GUL452'}, {'id': 'GUL453', 'label': 'GUL453'}, {'id': 'GUL454', 'label': 'GUL454'}, {'id': 'GUL455', 'label': 'GUL455'}, {'id': 'GUL456', 'label': 'GUL456'}, {'id': 'GUL457', 'label': 'GUL457'}, {'id': 'GUL458', 'label': 'GUL458'}, {'id': 'GUL459', 'label': 'GUL459'}, {'id': 'GUL460', 'label': 'GUL460'}, {'id': 'GUL461', 'label': 'GUL461'}, {'id': 'GUL462', 'label': 'GUL462'}, {'id': 'GUL463', 'label': 'GUL463'}, {'id': 'GUL464', 'label': 'GUL464'}, {'id': 'GUL465', 'label': 'GUL465'}, {'id': 'GUL466', 'label': 'GUL466'}, {'id': 'GUL467', 'label': 'GUL467'}, {'id': 'GUL468', 'label': 'GUL468'}, {'id': 'GUL469', 'label': 'GUL469'}, {'id': 'GUL470', 'label': 'GUL470'}, {'id': 'GUL471', 'label': 'GUL471'}, {'id': 'GUL472', 'label': 'GUL472'}, {'id': 'GUL473', 'label': 'GUL473'}, {'id': 'GUL474', 'label': 'GUL474'}, {'id': 'GUL475', 'label': 'GUL475'}, {'id': 'GUL476', 'label': 'GUL476'}, {'id': 'GUL477', 'label': 'GUL477'}, {'id': 'GUL478', 'label': 'GUL478'}, {'id': 'GUL479', 'label': 'GUL479'}, {'id': 'GUL480', 'label': 'GUL480'}, {'id': 'GUL481', 'label': 'GUL481'}, {'id': 'GUL482', 'label': 'GUL482'}, {'id': 'GUL483', 'label': 'GUL483'}, {'id': 'GUL484', 'label': 'GUL484'}, {'id': 'GUL485', 'label': 'GUL485'}, {'id': 'GUL486', 'label': 'GUL486'}, {'id': 'GUL487', 'label': 'GUL487'}, {'id': 'GUL488', 'label': 'GUL488'}, {'id': 'GUL489', 'label': 'GUL489'}, {'id': 'GUL490', 'label': 'GUL490'}, {'id': 'GUL491', 'label': 'GUL491'}, {'id': 'GUL492', 'label': 'GUL492'}, {'id': 'GUL493', 'label': 'GUL493'}, {'id': 'GUL494', 'label': 'GUL494'}, {'id': 'GUL495', 'label': 'GUL495'}, {'id': 'GUL496', 'label': 'GUL496'}, {'id': 'GUL497', 'label': 'GUL497'}, {'id': 'GUL498', 'label': 'GUL498'}, {'id': 'GUL499', 'label': 'GUL499'}, {'id': 'GUL500', 'label': 'GUL500'}]//, {'id': 'GUL501', 'label': 'GUL501'}, {'id': 'GUL502', 'label': 'GUL502'}, {'id': 'GUL503', 'label': 'GUL503'}, {'id': 'GUL504', 'label': 'GUL504'}, {'id': 'GUL505', 'label': 'GUL505'}, {'id': 'GUL506', 'label': 'GUL506'}, {'id': 'GUL507', 'label': 'GUL507'}, {'id': 'GUL508', 'label': 'GUL508'}, {'id': 'GUL509', 'label': 'GUL509'}, {'id': 'GUL510', 'label': 'GUL510'}, {'id': 'GUL511', 'label': 'GUL511'}, {'id': 'GUL512', 'label': 'GUL512'}, {'id': 'GUL513', 'label': 'GUL513'}, {'id': 'GUL514', 'label': 'GUL514'}, {'id': 'GUL515', 'label': 'GUL515'}, {'id': 'GUL516', 'label': 'GUL516'}, {'id': 'GUL517', 'label': 'GUL517'}, {'id': 'GUL518', 'label': 'GUL518'}, {'id': 'GUL519', 'label': 'GUL519'}, {'id': 'GUL520', 'label': 'GUL520'}, {'id': 'GUL521', 'label': 'GUL521'}, {'id': 'GUL522', 'label': 'GUL522'}, {'id': 'GUL523', 'label': 'GUL523'}, {'id': 'GUL524', 'label': 'GUL524'}, {'id': 'GUL525', 'label': 'GUL525'}, {'id': 'GUL526', 'label': 'GUL526'}, {'id': 'GUL527', 'label': 'GUL527'}, {'id': 'GUL528', 'label': 'GUL528'}, {'id': 'GUL529', 'label': 'GUL529'}, {'id': 'GUL530', 'label': 'GUL530'}, {'id': 'GUL531', 'label': 'GUL531'}, {'id': 'GUL532', 'label': 'GUL532'}, {'id': 'GUL533', 'label': 'GUL533'}, {'id': 'GUL534', 'label': 'GUL534'}, {'id': 'GUL535', 'label': 'GUL535'}, {'id': 'GUL536', 'label': 'GUL536'}, {'id': 'GUL537', 'label': 'GUL537'}, {'id': 'GUL538', 'label': 'GUL538'}, {'id': 'GUL539', 'label': 'GUL539'}, {'id': 'GUL540', 'label': 'GUL540'}, {'id': 'GUL541', 'label': 'GUL541'}, {'id': 'GUL542', 'label': 'GUL542'}, {'id': 'GUL543', 'label': 'GUL543'}, {'id': 'GUL544', 'label': 'GUL544'}, {'id': 'GUL545', 'label': 'GUL545'}, {'id': 'GUL546', 'label': 'GUL546'}, {'id': 'GUL547', 'label': 'GUL547'}, {'id': 'GUL548', 'label': 'GUL548'}, {'id': 'GUL549', 'label': 'GUL549'}, {'id': 'GUL550', 'label': 'GUL550'}, {'id': 'GUL551', 'label': 'GUL551'}, {'id': 'GUL552', 'label': 'GUL552'}, {'id': 'GUL553', 'label': 'GUL553'}, {'id': 'GUL554', 'label': 'GUL554'}, {'id': 'GUL555', 'label': 'GUL555'}, {'id': 'GUL556', 'label': 'GUL556'}, {'id': 'GUL557', 'label': 'GUL557'}, {'id': 'GUL558', 'label': 'GUL558'}, {'id': 'GUL559', 'label': 'GUL559'}, {'id': 'GUL560', 'label': 'GUL560'}, {'id': 'GUL561', 'label': 'GUL561'}, {'id': 'GUL562', 'label': 'GUL562'}, {'id': 'GUL563', 'label': 'GUL563'}, {'id': 'GUL564', 'label': 'GUL564'}, {'id': 'GUL565', 'label': 'GUL565'}, {'id': 'GUL566', 'label': 'GUL566'}, {'id': 'GUL567', 'label': 'GUL567'}, {'id': 'GUL568', 'label': 'GUL568'}, {'id': 'GUL569', 'label': 'GUL569'}, {'id': 'GUL570', 'label': 'GUL570'}, {'id': 'GUL571', 'label': 'GUL571'}, {'id': 'GUL572', 'label': 'GUL572'}, {'id': 'GUL573', 'label': 'GUL573'}, {'id': 'GUL574', 'label': 'GUL574'}, {'id': 'GUL575', 'label': 'GUL575'}, {'id': 'GUL576', 'label': 'GUL576'}, {'id': 'GUL577', 'label': 'GUL577'}, {'id': 'GUL578', 'label': 'GUL578'}, {'id': 'GUL579', 'label': 'GUL579'}, {'id': 'GUL580', 'label': 'GUL580'}, {'id': 'GUL581', 'label': 'GUL581'}, {'id': 'GUL582', 'label': 'GUL582'}, {'id': 'GUL583', 'label': 'GUL583'}, {'id': 'GUL584', 'label': 'GUL584'}, {'id': 'GUL585', 'label': 'GUL585'}, {'id': 'GUL586', 'label': 'GUL586'}, {'id': 'GUL587', 'label': 'GUL587'}, {'id': 'GUL588', 'label': 'GUL588'}, {'id': 'GUL589', 'label': 'GUL589'}, {'id': 'GUL590', 'label': 'GUL590'}, {'id': 'GUL591', 'label': 'GUL591'}, {'id': 'GUL592', 'label': 'GUL592'}, {'id': 'GUL593', 'label': 'GUL593'}, {'id': 'GUL594', 'label': 'GUL594'}, {'id': 'GUL595', 'label': 'GUL595'}, {'id': 'GUL596', 'label': 'GUL596'}, {'id': 'GUL597', 'label': 'GUL597'}, {'id': 'GUL598', 'label': 'GUL598'}, {'id': 'GUL599', 'label': 'GUL599'}, {'id': 'GUL600', 'label': 'GUL600'}, {'id': 'GUL601', 'label': 'GUL601'}, {'id': 'GUL602', 'label': 'GUL602'}, {'id': 'GUL603', 'label': 'GUL603'}, {'id': 'GUL604', 'label': 'GUL604'}, {'id': 'GUL605', 'label': 'GUL605'}, {'id': 'GUL606', 'label': 'GUL606'}, {'id': 'GUL607', 'label': 'GUL607'}, {'id': 'GUL608', 'label': 'GUL608'}, {'id': 'GUL609', 'label': 'GUL609'}, {'id': 'GUL610', 'label': 'GUL610'}, {'id': 'GUL611', 'label': 'GUL611'}, {'id': 'GUL612', 'label': 'GUL612'}, {'id': 'GUL613', 'label': 'GUL613'}, {'id': 'GUL614', 'label': 'GUL614'}, {'id': 'GUL615', 'label': 'GUL615'}, {'id': 'GUL616', 'label': 'GUL616'}, {'id': 'GUL617', 'label': 'GUL617'}, {'id': 'GUL618', 'label': 'GUL618'}, {'id': 'GUL619', 'label': 'GUL619'}, {'id': 'GUL620', 'label': 'GUL620'}, {'id': 'GUL621', 'label': 'GUL621'}, {'id': 'GUL622', 'label': 'GUL622'}, {'id': 'GUL623', 'label': 'GUL623'}, {'id': 'GUL624', 'label': 'GUL624'}, {'id': 'GUL625', 'label': 'GUL625'}, {'id': 'GUL626', 'label': 'GUL626'}, {'id': 'GUL627', 'label': 'GUL627'}, {'id': 'GUL628', 'label': 'GUL628'}, {'id': 'GUL629', 'label': 'GUL629'}, {'id': 'GUL630', 'label': 'GUL630'}, {'id': 'GUL631', 'label': 'GUL631'}, {'id': 'GUL632', 'label': 'GUL632'}, {'id': 'GUL633', 'label': 'GUL633'}, {'id': 'GUL634', 'label': 'GUL634'}, {'id': 'GUL635', 'label': 'GUL635'}, {'id': 'GUL636', 'label': 'GUL636'}, {'id': 'GUL637', 'label': 'GUL637'}, {'id': 'GUL638', 'label': 'GUL638'}, {'id': 'GUL639', 'label': 'GUL639'}, {'id': 'GUL640', 'label': 'GUL640'}, {'id': 'GUL641', 'label': 'GUL641'}, {'id': 'GUL642', 'label': 'GUL642'}, {'id': 'GUL643', 'label': 'GUL643'}, {'id': 'GUL644', 'label': 'GUL644'}, {'id': 'GUL645', 'label': 'GUL645'}, {'id': 'GUL646', 'label': 'GUL646'}, {'id': 'GUL647', 'label': 'GUL647'}, {'id': 'GUL648', 'label': 'GUL648'}, {'id': 'GUL649', 'label': 'GUL649'}, {'id': 'GUL650', 'label': 'GUL650'}, {'id': 'GUL651', 'label': 'GUL651'}, {'id': 'GUL652', 'label': 'GUL652'}, {'id': 'GUL653', 'label': 'GUL653'}, {'id': 'GUL654', 'label': 'GUL654'}, {'id': 'GUL655', 'label': 'GUL655'}, {'id': 'GUL656', 'label': 'GUL656'}, {'id': 'GUL657', 'label': 'GUL657'}, {'id': 'GUL658', 'label': 'GUL658'}, {'id': 'GUL659', 'label': 'GUL659'}, {'id': 'GUL660', 'label': 'GUL660'}, {'id': 'GUL661', 'label': 'GUL661'}, {'id': 'GUL662', 'label': 'GUL662'}, {'id': 'GUL663', 'label': 'GUL663'}, {'id': 'GUL664', 'label': 'GUL664'}, {'id': 'GUL665', 'label': 'GUL665'}, {'id': 'GUL666', 'label': 'GUL666'}, {'id': 'GUL667', 'label': 'GUL667'}, {'id': 'GUL668', 'label': 'GUL668'}, {'id': 'GUL669', 'label': 'GUL669'}, {'id': 'GUL670', 'label': 'GUL670'}, {'id': 'GUL671', 'label': 'GUL671'}, {'id': 'GUL672', 'label': 'GUL672'}, {'id': 'GUL673', 'label': 'GUL673'}, {'id': 'GUL674', 'label': 'GUL674'}, {'id': 'GUL675', 'label': 'GUL675'}, {'id': 'GUL676', 'label': 'GUL676'}, {'id': 'GUL677', 'label': 'GUL677'}, {'id': 'GUL678', 'label': 'GUL678'}, {'id': 'GUL679', 'label': 'GUL679'}, {'id': 'GUL680', 'label': 'GUL680'}, {'id': 'GUL681', 'label': 'GUL681'}, {'id': 'GUL682', 'label': 'GUL682'}, {'id': 'GUL683', 'label': 'GUL683'}, {'id': 'GUL684', 'label': 'GUL684'}, {'id': 'GUL685', 'label': 'GUL685'}, {'id': 'GUL686', 'label': 'GUL686'}, {'id': 'GUL687', 'label': 'GUL687'}, {'id': 'GUL688', 'label': 'GUL688'}, {'id': 'GUL689', 'label': 'GUL689'}, {'id': 'GUL690', 'label': 'GUL690'}, {'id': 'GUL691', 'label': 'GUL691'}, {'id': 'GUL692', 'label': 'GUL692'}, {'id': 'GUL693', 'label': 'GUL693'}, {'id': 'GUL694', 'label': 'GUL694'}, {'id': 'GUL695', 'label': 'GUL695'}, {'id': 'GUL696', 'label': 'GUL696'}, {'id': 'GUL697', 'label': 'GUL697'}, {'id': 'GUL698', 'label': 'GUL698'}, {'id': 'GUL699', 'label': 'GUL699'}, {'id': 'GUL700', 'label': 'GUL700'}, {'id': 'GUL701', 'label': 'GUL701'}, {'id': 'GUL702', 'label': 'GUL702'}, {'id': 'GUL703', 'label': 'GUL703'}, {'id': 'GUL704', 'label': 'GUL704'}, {'id': 'GUL705', 'label': 'GUL705'}, {'id': 'GUL706', 'label': 'GUL706'}, {'id': 'GUL707', 'label': 'GUL707'}, {'id': 'GUL708', 'label': 'GUL708'}, {'id': 'GUL709', 'label': 'GUL709'}, {'id': 'GUL710', 'label': 'GUL710'}, {'id': 'GUL711', 'label': 'GUL711'}, {'id': 'GUL712', 'label': 'GUL712'}, {'id': 'GUL713', 'label': 'GUL713'}, {'id': 'GUL714', 'label': 'GUL714'}, {'id': 'GUL715', 'label': 'GUL715'}, {'id': 'GUL716', 'label': 'GUL716'}, {'id': 'GUL717', 'label': 'GUL717'}, {'id': 'GUL718', 'label': 'GUL718'}, {'id': 'GUL719', 'label': 'GUL719'}, {'id': 'GUL720', 'label': 'GUL720'}, {'id': 'GUL721', 'label': 'GUL721'}, {'id': 'GUL722', 'label': 'GUL722'}, {'id': 'GUL723', 'label': 'GUL723'}, {'id': 'GUL724', 'label': 'GUL724'}, {'id': 'GUL725', 'label': 'GUL725'}, {'id': 'GUL726', 'label': 'GUL726'}, {'id': 'GUL727', 'label': 'GUL727'}, {'id': 'GUL728', 'label': 'GUL728'}, {'id': 'GUL729', 'label': 'GUL729'}, {'id': 'GUL730', 'label': 'GUL730'}, {'id': 'GUL731', 'label': 'GUL731'}, {'id': 'GUL732', 'label': 'GUL732'}, {'id': 'GUL733', 'label': 'GUL733'}, {'id': 'GUL734', 'label': 'GUL734'}, {'id': 'GUL735', 'label': 'GUL735'}, {'id': 'GUL736', 'label': 'GUL736'}, {'id': 'GUL737', 'label': 'GUL737'}, {'id': 'GUL738', 'label': 'GUL738'}, {'id': 'GUL739', 'label': 'GUL739'}, {'id': 'GUL740', 'label': 'GUL740'}, {'id': 'GUL741', 'label': 'GUL741'}, {'id': 'GUL742', 'label': 'GUL742'}, {'id': 'GUL743', 'label': 'GUL743'}, {'id': 'GUL744', 'label': 'GUL744'}, {'id': 'GUL745', 'label': 'GUL745'}, {'id': 'GUL746', 'label': 'GUL746'}, {'id': 'GUL747', 'label': 'GUL747'}, {'id': 'GUL748', 'label': 'GUL748'}, {'id': 'GUL749', 'label': 'GUL749'}, {'id': 'GUL750', 'label': 'GUL750'}, {'id': 'GUL751', 'label': 'GUL751'}, {'id': 'GUL752', 'label': 'GUL752'}, {'id': 'GUL753', 'label': 'GUL753'}, {'id': 'GUL754', 'label': 'GUL754'}, {'id': 'GUL755', 'label': 'GUL755'}, {'id': 'GUL756', 'label': 'GUL756'}, {'id': 'GUL757', 'label': 'GUL757'}, {'id': 'GUL758', 'label': 'GUL758'}, {'id': 'GUL759', 'label': 'GUL759'}, {'id': 'GUL760', 'label': 'GUL760'}, {'id': 'GUL761', 'label': 'GUL761'}, {'id': 'GUL762', 'label': 'GUL762'}, {'id': 'GUL763', 'label': 'GUL763'}, {'id': 'GUL764', 'label': 'GUL764'}, {'id': 'GUL765', 'label': 'GUL765'}, {'id': 'GUL766', 'label': 'GUL766'}, {'id': 'GUL767', 'label': 'GUL767'}, {'id': 'GUL768', 'label': 'GUL768'}, {'id': 'GUL769', 'label': 'GUL769'}, {'id': 'GUL770', 'label': 'GUL770'}, {'id': 'GUL771', 'label': 'GUL771'}, {'id': 'GUL772', 'label': 'GUL772'}, {'id': 'GUL773', 'label': 'GUL773'}, {'id': 'GUL774', 'label': 'GUL774'}, {'id': 'GUL775', 'label': 'GUL775'}, {'id': 'GUL776', 'label': 'GUL776'}, {'id': 'GUL777', 'label': 'GUL777'}, {'id': 'GUL778', 'label': 'GUL778'}, {'id': 'GUL779', 'label': 'GUL779'}, {'id': 'GUL780', 'label': 'GUL780'}, {'id': 'GUL781', 'label': 'GUL781'}, {'id': 'GUL782', 'label': 'GUL782'}, {'id': 'GUL783', 'label': 'GUL783'}, {'id': 'GUL784', 'label': 'GUL784'}, {'id': 'GUL785', 'label': 'GUL785'}, {'id': 'GUL786', 'label': 'GUL786'}, {'id': 'GUL787', 'label': 'GUL787'}, {'id': 'GUL788', 'label': 'GUL788'}, {'id': 'GUL789', 'label': 'GUL789'}, {'id': 'GUL790', 'label': 'GUL790'}, {'id': 'GUL791', 'label': 'GUL791'}, {'id': 'GUL792', 'label': 'GUL792'}, {'id': 'GUL793', 'label': 'GUL793'}, {'id': 'GUL794', 'label': 'GUL794'}, {'id': 'GUL795', 'label': 'GUL795'}, {'id': 'GUL796', 'label': 'GUL796'}, {'id': 'GUL797', 'label': 'GUL797'}, {'id': 'GUL798', 'label': 'GUL798'}, {'id': 'GUL799', 'label': 'GUL799'}, {'id': 'GUL800', 'label': 'GUL800'}, {'id': 'GUL801', 'label': 'GUL801'}, {'id': 'GUL802', 'label': 'GUL802'}, {'id': 'GUL803', 'label': 'GUL803'}, {'id': 'GUL804', 'label': 'GUL804'}, {'id': 'GUL805', 'label': 'GUL805'}, {'id': 'GUL806', 'label': 'GUL806'}, {'id': 'GUL807', 'label': 'GUL807'}, {'id': 'GUL808', 'label': 'GUL808'}, {'id': 'GUL809', 'label': 'GUL809'}, {'id': 'GUL810', 'label': 'GUL810'}, {'id': 'GUL811', 'label': 'GUL811'}, {'id': 'GUL812', 'label': 'GUL812'}, {'id': 'GUL813', 'label': 'GUL813'}, {'id': 'GUL814', 'label': 'GUL814'}, {'id': 'GUL815', 'label': 'GUL815'}, {'id': 'GUL816', 'label': 'GUL816'}, {'id': 'GUL817', 'label': 'GUL817'}, {'id': 'GUL818', 'label': 'GUL818'}, {'id': 'GUL819', 'label': 'GUL819'}, {'id': 'GUL820', 'label': 'GUL820'}, {'id': 'GUL821', 'label': 'GUL821'}, {'id': 'GUL822', 'label': 'GUL822'}, {'id': 'GUL823', 'label': 'GUL823'}, {'id': 'GUL824', 'label': 'GUL824'}, {'id': 'GUL825', 'label': 'GUL825'}, {'id': 'GUL826', 'label': 'GUL826'}, {'id': 'GUL827', 'label': 'GUL827'}, {'id': 'GUL828', 'label': 'GUL828'}, {'id': 'GUL829', 'label': 'GUL829'}, {'id': 'GUL830', 'label': 'GUL830'}, {'id': 'GUL831', 'label': 'GUL831'}, {'id': 'GUL832', 'label': 'GUL832'}, {'id': 'GUL833', 'label': 'GUL833'}, {'id': 'GUL834', 'label': 'GUL834'}, {'id': 'GUL835', 'label': 'GUL835'}, {'id': 'GUL836', 'label': 'GUL836'}, {'id': 'GUL837', 'label': 'GUL837'}, {'id': 'GUL838', 'label': 'GUL838'}, {'id': 'GUL839', 'label': 'GUL839'}, {'id': 'GUL840', 'label': 'GUL840'}, {'id': 'GUL841', 'label': 'GUL841'}, {'id': 'GUL842', 'label': 'GUL842'}, {'id': 'GUL843', 'label': 'GUL843'}, {'id': 'GUL844', 'label': 'GUL844'}, {'id': 'GUL845', 'label': 'GUL845'}, {'id': 'GUL846', 'label': 'GUL846'}, {'id': 'GUL847', 'label': 'GUL847'}, {'id': 'GUL848', 'label': 'GUL848'}, {'id': 'GUL849', 'label': 'GUL849'}, {'id': 'GUL850', 'label': 'GUL850'}, {'id': 'GUL851', 'label': 'GUL851'}, {'id': 'GUL852', 'label': 'GUL852'}, {'id': 'GUL853', 'label': 'GUL853'}, {'id': 'GUL854', 'label': 'GUL854'}, {'id': 'GUL855', 'label': 'GUL855'}, {'id': 'GUL856', 'label': 'GUL856'}, {'id': 'GUL857', 'label': 'GUL857'}, {'id': 'GUL858', 'label': 'GUL858'}, {'id': 'GUL859', 'label': 'GUL859'}, {'id': 'GUL860', 'label': 'GUL860'}, {'id': 'GUL861', 'label': 'GUL861'}, {'id': 'GUL862', 'label': 'GUL862'}, {'id': 'GUL863', 'label': 'GUL863'}, {'id': 'GUL864', 'label': 'GUL864'}, {'id': 'GUL865', 'label': 'GUL865'}, {'id': 'GUL866', 'label': 'GUL866'}, {'id': 'GUL867', 'label': 'GUL867'}, {'id': 'GUL868', 'label': 'GUL868'}, {'id': 'GUL869', 'label': 'GUL869'}, {'id': 'GUL870', 'label': 'GUL870'}, {'id': 'GUL871', 'label': 'GUL871'}, {'id': 'GUL872', 'label': 'GUL872'}, {'id': 'GUL873', 'label': 'GUL873'}, {'id': 'GUL874', 'label': 'GUL874'}, {'id': 'GUL875', 'label': 'GUL875'}, {'id': 'GUL876', 'label': 'GUL876'}, {'id': 'GUL877', 'label': 'GUL877'}, {'id': 'GUL878', 'label': 'GUL878'}, {'id': 'GUL879', 'label': 'GUL879'}, {'id': 'GUL880', 'label': 'GUL880'}, {'id': 'GUL881', 'label': 'GUL881'}, {'id': 'GUL882', 'label': 'GUL882'}, {'id': 'GUL883', 'label': 'GUL883'}, {'id': 'GUL884', 'label': 'GUL884'}, {'id': 'GUL885', 'label': 'GUL885'}, {'id': 'GUL886', 'label': 'GUL886'}, {'id': 'GUL887', 'label': 'GUL887'}, {'id': 'GUL888', 'label': 'GUL888'}, {'id': 'GUL889', 'label': 'GUL889'}, {'id': 'GUL890', 'label': 'GUL890'}, {'id': 'GUL891', 'label': 'GUL891'}, {'id': 'GUL892', 'label': 'GUL892'}, {'id': 'GUL893', 'label': 'GUL893'}, {'id': 'GUL894', 'label': 'GUL894'}, {'id': 'GUL895', 'label': 'GUL895'}, {'id': 'GUL896', 'label': 'GUL896'}, {'id': 'GUL897', 'label': 'GUL897'}, {'id': 'GUL898', 'label': 'GUL898'}, {'id': 'GUL899', 'label': 'GUL899'}, {'id': 'GUL900', 'label': 'GUL900'}, {'id': 'GUL901', 'label': 'GUL901'}, {'id': 'GUL902', 'label': 'GUL902'}, {'id': 'GUL903', 'label': 'GUL903'}, {'id': 'GUL904', 'label': 'GUL904'}, {'id': 'GUL905', 'label': 'GUL905'}, {'id': 'GUL906', 'label': 'GUL906'}, {'id': 'GUL907', 'label': 'GUL907'}, {'id': 'GUL908', 'label': 'GUL908'}, {'id': 'GUL909', 'label': 'GUL909'}, {'id': 'GUL910', 'label': 'GUL910'}, {'id': 'GUL911', 'label': 'GUL911'}, {'id': 'GUL912', 'label': 'GUL912'}, {'id': 'GUL913', 'label': 'GUL913'}, {'id': 'GUL914', 'label': 'GUL914'}, {'id': 'GUL915', 'label': 'GUL915'}, {'id': 'GUL916', 'label': 'GUL916'}, {'id': 'GUL917', 'label': 'GUL917'}, {'id': 'GUL918', 'label': 'GUL918'}, {'id': 'GUL919', 'label': 'GUL919'}, {'id': 'GUL920', 'label': 'GUL920'}, {'id': 'GUL921', 'label': 'GUL921'}, {'id': 'GUL922', 'label': 'GUL922'}, {'id': 'GUL923', 'label': 'GUL923'}, {'id': 'GUL924', 'label': 'GUL924'}, {'id': 'GUL925', 'label': 'GUL925'}, {'id': 'GUL926', 'label': 'GUL926'}, {'id': 'GUL927', 'label': 'GUL927'}, {'id': 'GUL928', 'label': 'GUL928'}, {'id': 'GUL929', 'label': 'GUL929'}, {'id': 'GUL930', 'label': 'GUL930'}, {'id': 'GUL931', 'label': 'GUL931'}, {'id': 'GUL932', 'label': 'GUL932'}, {'id': 'GUL933', 'label': 'GUL933'}, {'id': 'GUL934', 'label': 'GUL934'}, {'id': 'GUL935', 'label': 'GUL935'}, {'id': 'GUL936', 'label': 'GUL936'}, {'id': 'GUL937', 'label': 'GUL937'}, {'id': 'GUL938', 'label': 'GUL938'}, {'id': 'GUL939', 'label': 'GUL939'}, {'id': 'GUL940', 'label': 'GUL940'}, {'id': 'GUL941', 'label': 'GUL941'}, {'id': 'GUL942', 'label': 'GUL942'}, {'id': 'GUL943', 'label': 'GUL943'}, {'id': 'GUL944', 'label': 'GUL944'}, {'id': 'GUL945', 'label': 'GUL945'}, {'id': 'GUL946', 'label': 'GUL946'}, {'id': 'GUL947', 'label': 'GUL947'}, {'id': 'GUL948', 'label': 'GUL948'}, {'id': 'GUL949', 'label': 'GUL949'}, {'id': 'GUL950', 'label': 'GUL950'}, {'id': 'GUL951', 'label': 'GUL951'}, {'id': 'GUL952', 'label': 'GUL952'}, {'id': 'GUL953', 'label': 'GUL953'}, {'id': 'GUL954', 'label': 'GUL954'}, {'id': 'GUL955', 'label': 'GUL955'}, {'id': 'GUL956', 'label': 'GUL956'}, {'id': 'GUL957', 'label': 'GUL957'}, {'id': 'GUL958', 'label': 'GUL958'}, {'id': 'GUL959', 'label': 'GUL959'}, {'id': 'GUL960', 'label': 'GUL960'}, {'id': 'GUL961', 'label': 'GUL961'}, {'id': 'GUL962', 'label': 'GUL962'}, {'id': 'GUL963', 'label': 'GUL963'}, {'id': 'GUL964', 'label': 'GUL964'}, {'id': 'GUL965', 'label': 'GUL965'}, {'id': 'GUL966', 'label': 'GUL966'}, {'id': 'GUL967', 'label': 'GUL967'}, {'id': 'GUL968', 'label': 'GUL968'}, {'id': 'GUL969', 'label': 'GUL969'}, {'id': 'GUL970', 'label': 'GUL970'}, {'id': 'GUL971', 'label': 'GUL971'}, {'id': 'GUL972', 'label': 'GUL972'}, {'id': 'GUL973', 'label': 'GUL973'}, {'id': 'GUL974', 'label': 'GUL974'}, {'id': 'GUL975', 'label': 'GUL975'}, {'id': 'GUL976', 'label': 'GUL976'}, {'id': 'GUL977', 'label': 'GUL977'}, {'id': 'GUL978', 'label': 'GUL978'}, {'id': 'GUL979', 'label': 'GUL979'}, {'id': 'GUL980', 'label': 'GUL980'}, {'id': 'GUL981', 'label': 'GUL981'}, {'id': 'GUL982', 'label': 'GUL982'}, {'id': 'GUL983', 'label': 'GUL983'}, {'id': 'GUL984', 'label': 'GUL984'}, {'id': 'GUL985', 'label': 'GUL985'}, {'id': 'GUL986', 'label': 'GUL986'}, {'id': 'GUL987', 'label': 'GUL987'}, {'id': 'GUL988', 'label': 'GUL988'}, {'id': 'GUL989', 'label': 'GUL989'}, {'id': 'GUL990', 'label': 'GUL990'}, {'id': 'GUL991', 'label': 'GUL991'}, {'id': 'GUL992', 'label': 'GUL992'}, {'id': 'GUL993', 'label': 'GUL993'}, {'id': 'GUL994', 'label': 'GUL994'}, {'id': 'GUL995', 'label': 'GUL995'}, {'id': 'GUL996', 'label': 'GUL996'}, {'id': 'GUL997', 'label': 'GUL997'}, {'id': 'GUL998', 'label': 'GUL998'}, {'id': 'GUL999', 'label': 'GUL999'}, {'id': 'GUL1000', 'label': 'GUL1000'}]
                                };
                        }
                        if (row === 3){
                            cellProperties.renderer = customDropdownRenderer;
                            cellProperties.editor = "chosen";
                            cellProperties.width = 500;
                            cellProperties.chosenOptions ={
                                multiple: true,
                                data: [{'id': 'GUL1', 'label': 'GUL1'}, {'id': 'GUL2', 'label': 'GUL2'}, {'id': 'GUL3', 'label': 'GUL3'}, {'id': 'GUL4', 'label': 'GUL4'}, {'id': 'GUL5', 'label': 'GUL5'}, {'id': 'GUL6', 'label': 'GUL6'}, {'id': 'GUL7', 'label': 'GUL7'}, {'id': 'GUL8', 'label': 'GUL8'}, {'id': 'GUL9', 'label': 'GUL9'}, {'id': 'GUL10', 'label': 'GUL10'}, {'id': 'GUL11', 'label': 'GUL11'}, {'id': 'GUL12', 'label': 'GUL12'}, {'id': 'GUL13', 'label': 'GUL13'}, {'id': 'GUL14', 'label': 'GUL14'}, {'id': 'GUL15', 'label': 'GUL15'}, {'id': 'GUL16', 'label': 'GUL16'}, {'id': 'GUL17', 'label': 'GUL17'}, {'id': 'GUL18', 'label': 'GUL18'}, {'id': 'GUL19', 'label': 'GUL19'}, {'id': 'GUL20', 'label': 'GUL20'}, {'id': 'GUL21', 'label': 'GUL21'}, {'id': 'GUL22', 'label': 'GUL22'}, {'id': 'GUL23', 'label': 'GUL23'}, {'id': 'GUL24', 'label': 'GUL24'}, {'id': 'GUL25', 'label': 'GUL25'}, {'id': 'GUL26', 'label': 'GUL26'}, {'id': 'GUL27', 'label': 'GUL27'}, {'id': 'GUL28', 'label': 'GUL28'}, {'id': 'GUL29', 'label': 'GUL29'}, {'id': 'GUL30', 'label': 'GUL30'}, {'id': 'GUL31', 'label': 'GUL31'}, {'id': 'GUL32', 'label': 'GUL32'}, {'id': 'GUL33', 'label': 'GUL33'}, {'id': 'GUL34', 'label': 'GUL34'}, {'id': 'GUL35', 'label': 'GUL35'}, {'id': 'GUL36', 'label': 'GUL36'}, {'id': 'GUL37', 'label': 'GUL37'}, {'id': 'GUL38', 'label': 'GUL38'}, {'id': 'GUL39', 'label': 'GUL39'}, {'id': 'GUL40', 'label': 'GUL40'}, {'id': 'GUL41', 'label': 'GUL41'}, {'id': 'GUL42', 'label': 'GUL42'}, {'id': 'GUL43', 'label': 'GUL43'}, {'id': 'GUL44', 'label': 'GUL44'}, {'id': 'GUL45', 'label': 'GUL45'}, {'id': 'GUL46', 'label': 'GUL46'}, {'id': 'GUL47', 'label': 'GUL47'}, {'id': 'GUL48', 'label': 'GUL48'}, {'id': 'GUL49', 'label': 'GUL49'}, {'id': 'GUL50', 'label': 'GUL50'}, {'id': 'GUL51', 'label': 'GUL51'}, {'id': 'GUL52', 'label': 'GUL52'}, {'id': 'GUL53', 'label': 'GUL53'}, {'id': 'GUL54', 'label': 'GUL54'}, {'id': 'GUL55', 'label': 'GUL55'}, {'id': 'GUL56', 'label': 'GUL56'}, {'id': 'GUL57', 'label': 'GUL57'}, {'id': 'GUL58', 'label': 'GUL58'}, {'id': 'GUL59', 'label': 'GUL59'}, {'id': 'GUL60', 'label': 'GUL60'}, {'id': 'GUL61', 'label': 'GUL61'}, {'id': 'GUL62', 'label': 'GUL62'}, {'id': 'GUL63', 'label': 'GUL63'}, {'id': 'GUL64', 'label': 'GUL64'}, {'id': 'GUL65', 'label': 'GUL65'}, {'id': 'GUL66', 'label': 'GUL66'}, {'id': 'GUL67', 'label': 'GUL67'}, {'id': 'GUL68', 'label': 'GUL68'}, {'id': 'GUL69', 'label': 'GUL69'}, {'id': 'GUL70', 'label': 'GUL70'}, {'id': 'GUL71', 'label': 'GUL71'}, {'id': 'GUL72', 'label': 'GUL72'}, {'id': 'GUL73', 'label': 'GUL73'}, {'id': 'GUL74', 'label': 'GUL74'}, {'id': 'GUL75', 'label': 'GUL75'}, {'id': 'GUL76', 'label': 'GUL76'}, {'id': 'GUL77', 'label': 'GUL77'}, {'id': 'GUL78', 'label': 'GUL78'}, {'id': 'GUL79', 'label': 'GUL79'}, {'id': 'GUL80', 'label': 'GUL80'}, {'id': 'GUL81', 'label': 'GUL81'}, {'id': 'GUL82', 'label': 'GUL82'}, {'id': 'GUL83', 'label': 'GUL83'}, {'id': 'GUL84', 'label': 'GUL84'}, {'id': 'GUL85', 'label': 'GUL85'}, {'id': 'GUL86', 'label': 'GUL86'}, {'id': 'GUL87', 'label': 'GUL87'}, {'id': 'GUL88', 'label': 'GUL88'}, {'id': 'GUL89', 'label': 'GUL89'}, {'id': 'GUL90', 'label': 'GUL90'}, {'id': 'GUL91', 'label': 'GUL91'}, {'id': 'GUL92', 'label': 'GUL92'}, {'id': 'GUL93', 'label': 'GUL93'}, {'id': 'GUL94', 'label': 'GUL94'}, {'id': 'GUL95', 'label': 'GUL95'}, {'id': 'GUL96', 'label': 'GUL96'}, {'id': 'GUL97', 'label': 'GUL97'}, {'id': 'GUL98', 'label': 'GUL98'}, {'id': 'GUL99', 'label': 'GUL99'}, {'id': 'GUL100', 'label': 'GUL100'}, {'id': 'GUL101', 'label': 'GUL101'}, {'id': 'GUL102', 'label': 'GUL102'}, {'id': 'GUL103', 'label': 'GUL103'}, {'id': 'GUL104', 'label': 'GUL104'}, {'id': 'GUL105', 'label': 'GUL105'}, {'id': 'GUL106', 'label': 'GUL106'}, {'id': 'GUL107', 'label': 'GUL107'}, {'id': 'GUL108', 'label': 'GUL108'}, {'id': 'GUL109', 'label': 'GUL109'}, {'id': 'GUL110', 'label': 'GUL110'}, {'id': 'GUL111', 'label': 'GUL111'}, {'id': 'GUL112', 'label': 'GUL112'}, {'id': 'GUL113', 'label': 'GUL113'}, {'id': 'GUL114', 'label': 'GUL114'}, {'id': 'GUL115', 'label': 'GUL115'}, {'id': 'GUL116', 'label': 'GUL116'}, {'id': 'GUL117', 'label': 'GUL117'}, {'id': 'GUL118', 'label': 'GUL118'}, {'id': 'GUL119', 'label': 'GUL119'}, {'id': 'GUL120', 'label': 'GUL120'}, {'id': 'GUL121', 'label': 'GUL121'}, {'id': 'GUL122', 'label': 'GUL122'}, {'id': 'GUL123', 'label': 'GUL123'}, {'id': 'GUL124', 'label': 'GUL124'}, {'id': 'GUL125', 'label': 'GUL125'}, {'id': 'GUL126', 'label': 'GUL126'}, {'id': 'GUL127', 'label': 'GUL127'}, {'id': 'GUL128', 'label': 'GUL128'}, {'id': 'GUL129', 'label': 'GUL129'}, {'id': 'GUL130', 'label': 'GUL130'}, {'id': 'GUL131', 'label': 'GUL131'}, {'id': 'GUL132', 'label': 'GUL132'}, {'id': 'GUL133', 'label': 'GUL133'}, {'id': 'GUL134', 'label': 'GUL134'}, {'id': 'GUL135', 'label': 'GUL135'}, {'id': 'GUL136', 'label': 'GUL136'}, {'id': 'GUL137', 'label': 'GUL137'}, {'id': 'GUL138', 'label': 'GUL138'}, {'id': 'GUL139', 'label': 'GUL139'}, {'id': 'GUL140', 'label': 'GUL140'}, {'id': 'GUL141', 'label': 'GUL141'}, {'id': 'GUL142', 'label': 'GUL142'}, {'id': 'GUL143', 'label': 'GUL143'}, {'id': 'GUL144', 'label': 'GUL144'}, {'id': 'GUL145', 'label': 'GUL145'}, {'id': 'GUL146', 'label': 'GUL146'}, {'id': 'GUL147', 'label': 'GUL147'}, {'id': 'GUL148', 'label': 'GUL148'}, {'id': 'GUL149', 'label': 'GUL149'}, {'id': 'GUL150', 'label': 'GUL150'}, {'id': 'GUL151', 'label': 'GUL151'}, {'id': 'GUL152', 'label': 'GUL152'}, {'id': 'GUL153', 'label': 'GUL153'}, {'id': 'GUL154', 'label': 'GUL154'}, {'id': 'GUL155', 'label': 'GUL155'}, {'id': 'GUL156', 'label': 'GUL156'}, {'id': 'GUL157', 'label': 'GUL157'}, {'id': 'GUL158', 'label': 'GUL158'}, {'id': 'GUL159', 'label': 'GUL159'}, {'id': 'GUL160', 'label': 'GUL160'}, {'id': 'GUL161', 'label': 'GUL161'}, {'id': 'GUL162', 'label': 'GUL162'}, {'id': 'GUL163', 'label': 'GUL163'}, {'id': 'GUL164', 'label': 'GUL164'}, {'id': 'GUL165', 'label': 'GUL165'}, {'id': 'GUL166', 'label': 'GUL166'}, {'id': 'GUL167', 'label': 'GUL167'}, {'id': 'GUL168', 'label': 'GUL168'}, {'id': 'GUL169', 'label': 'GUL169'}, {'id': 'GUL170', 'label': 'GUL170'}, {'id': 'GUL171', 'label': 'GUL171'}, {'id': 'GUL172', 'label': 'GUL172'}, {'id': 'GUL173', 'label': 'GUL173'}, {'id': 'GUL174', 'label': 'GUL174'}, {'id': 'GUL175', 'label': 'GUL175'}, {'id': 'GUL176', 'label': 'GUL176'}, {'id': 'GUL177', 'label': 'GUL177'}, {'id': 'GUL178', 'label': 'GUL178'}, {'id': 'GUL179', 'label': 'GUL179'}, {'id': 'GUL180', 'label': 'GUL180'}, {'id': 'GUL181', 'label': 'GUL181'}, {'id': 'GUL182', 'label': 'GUL182'}, {'id': 'GUL183', 'label': 'GUL183'}, {'id': 'GUL184', 'label': 'GUL184'}, {'id': 'GUL185', 'label': 'GUL185'}, {'id': 'GUL186', 'label': 'GUL186'}, {'id': 'GUL187', 'label': 'GUL187'}, {'id': 'GUL188', 'label': 'GUL188'}, {'id': 'GUL189', 'label': 'GUL189'}, {'id': 'GUL190', 'label': 'GUL190'}, {'id': 'GUL191', 'label': 'GUL191'}, {'id': 'GUL192', 'label': 'GUL192'}, {'id': 'GUL193', 'label': 'GUL193'}, {'id': 'GUL194', 'label': 'GUL194'}, {'id': 'GUL195', 'label': 'GUL195'}, {'id': 'GUL196', 'label': 'GUL196'}, {'id': 'GUL197', 'label': 'GUL197'}, {'id': 'GUL198', 'label': 'GUL198'}, {'id': 'GUL199', 'label': 'GUL199'}, {'id': 'GUL200', 'label': 'GUL200'}, {'id': 'GUL201', 'label': 'GUL201'}, {'id': 'GUL202', 'label': 'GUL202'}, {'id': 'GUL203', 'label': 'GUL203'}, {'id': 'GUL204', 'label': 'GUL204'}, {'id': 'GUL205', 'label': 'GUL205'}, {'id': 'GUL206', 'label': 'GUL206'}, {'id': 'GUL207', 'label': 'GUL207'}, {'id': 'GUL208', 'label': 'GUL208'}, {'id': 'GUL209', 'label': 'GUL209'}, {'id': 'GUL210', 'label': 'GUL210'}, {'id': 'GUL211', 'label': 'GUL211'}, {'id': 'GUL212', 'label': 'GUL212'}, {'id': 'GUL213', 'label': 'GUL213'}, {'id': 'GUL214', 'label': 'GUL214'}, {'id': 'GUL215', 'label': 'GUL215'}, {'id': 'GUL216', 'label': 'GUL216'}, {'id': 'GUL217', 'label': 'GUL217'}, {'id': 'GUL218', 'label': 'GUL218'}, {'id': 'GUL219', 'label': 'GUL219'}, {'id': 'GUL220', 'label': 'GUL220'}, {'id': 'GUL221', 'label': 'GUL221'}, {'id': 'GUL222', 'label': 'GUL222'}, {'id': 'GUL223', 'label': 'GUL223'}, {'id': 'GUL224', 'label': 'GUL224'}, {'id': 'GUL225', 'label': 'GUL225'}, {'id': 'GUL226', 'label': 'GUL226'}, {'id': 'GUL227', 'label': 'GUL227'}, {'id': 'GUL228', 'label': 'GUL228'}, {'id': 'GUL229', 'label': 'GUL229'}, {'id': 'GUL230', 'label': 'GUL230'}, {'id': 'GUL231', 'label': 'GUL231'}, {'id': 'GUL232', 'label': 'GUL232'}, {'id': 'GUL233', 'label': 'GUL233'}, {'id': 'GUL234', 'label': 'GUL234'}, {'id': 'GUL235', 'label': 'GUL235'}, {'id': 'GUL236', 'label': 'GUL236'}, {'id': 'GUL237', 'label': 'GUL237'}, {'id': 'GUL238', 'label': 'GUL238'}, {'id': 'GUL239', 'label': 'GUL239'}, {'id': 'GUL240', 'label': 'GUL240'}, {'id': 'GUL241', 'label': 'GUL241'}, {'id': 'GUL242', 'label': 'GUL242'}, {'id': 'GUL243', 'label': 'GUL243'}, {'id': 'GUL244', 'label': 'GUL244'}, {'id': 'GUL245', 'label': 'GUL245'}, {'id': 'GUL246', 'label': 'GUL246'}, {'id': 'GUL247', 'label': 'GUL247'}, {'id': 'GUL248', 'label': 'GUL248'}, {'id': 'GUL249', 'label': 'GUL249'}, {'id': 'GUL250', 'label': 'GUL250'}, {'id': 'GUL251', 'label': 'GUL251'}, {'id': 'GUL252', 'label': 'GUL252'}, {'id': 'GUL253', 'label': 'GUL253'}, {'id': 'GUL254', 'label': 'GUL254'}, {'id': 'GUL255', 'label': 'GUL255'}, {'id': 'GUL256', 'label': 'GUL256'}, {'id': 'GUL257', 'label': 'GUL257'}, {'id': 'GUL258', 'label': 'GUL258'}, {'id': 'GUL259', 'label': 'GUL259'}, {'id': 'GUL260', 'label': 'GUL260'}, {'id': 'GUL261', 'label': 'GUL261'}, {'id': 'GUL262', 'label': 'GUL262'}, {'id': 'GUL263', 'label': 'GUL263'}, {'id': 'GUL264', 'label': 'GUL264'}, {'id': 'GUL265', 'label': 'GUL265'}, {'id': 'GUL266', 'label': 'GUL266'}, {'id': 'GUL267', 'label': 'GUL267'}, {'id': 'GUL268', 'label': 'GUL268'}, {'id': 'GUL269', 'label': 'GUL269'}, {'id': 'GUL270', 'label': 'GUL270'}, {'id': 'GUL271', 'label': 'GUL271'}, {'id': 'GUL272', 'label': 'GUL272'}, {'id': 'GUL273', 'label': 'GUL273'}, {'id': 'GUL274', 'label': 'GUL274'}, {'id': 'GUL275', 'label': 'GUL275'}, {'id': 'GUL276', 'label': 'GUL276'}, {'id': 'GUL277', 'label': 'GUL277'}, {'id': 'GUL278', 'label': 'GUL278'}, {'id': 'GUL279', 'label': 'GUL279'}, {'id': 'GUL280', 'label': 'GUL280'}, {'id': 'GUL281', 'label': 'GUL281'}, {'id': 'GUL282', 'label': 'GUL282'}, {'id': 'GUL283', 'label': 'GUL283'}, {'id': 'GUL284', 'label': 'GUL284'}, {'id': 'GUL285', 'label': 'GUL285'}, {'id': 'GUL286', 'label': 'GUL286'}, {'id': 'GUL287', 'label': 'GUL287'}, {'id': 'GUL288', 'label': 'GUL288'}, {'id': 'GUL289', 'label': 'GUL289'}, {'id': 'GUL290', 'label': 'GUL290'}, {'id': 'GUL291', 'label': 'GUL291'}, {'id': 'GUL292', 'label': 'GUL292'}, {'id': 'GUL293', 'label': 'GUL293'}, {'id': 'GUL294', 'label': 'GUL294'}, {'id': 'GUL295', 'label': 'GUL295'}, {'id': 'GUL296', 'label': 'GUL296'}, {'id': 'GUL297', 'label': 'GUL297'}, {'id': 'GUL298', 'label': 'GUL298'}, {'id': 'GUL299', 'label': 'GUL299'}, {'id': 'GUL300', 'label': 'GUL300'}, {'id': 'GUL301', 'label': 'GUL301'}, {'id': 'GUL302', 'label': 'GUL302'}, {'id': 'GUL303', 'label': 'GUL303'}, {'id': 'GUL304', 'label': 'GUL304'}, {'id': 'GUL305', 'label': 'GUL305'}, {'id': 'GUL306', 'label': 'GUL306'}, {'id': 'GUL307', 'label': 'GUL307'}, {'id': 'GUL308', 'label': 'GUL308'}, {'id': 'GUL309', 'label': 'GUL309'}, {'id': 'GUL310', 'label': 'GUL310'}, {'id': 'GUL311', 'label': 'GUL311'}, {'id': 'GUL312', 'label': 'GUL312'}, {'id': 'GUL313', 'label': 'GUL313'}, {'id': 'GUL314', 'label': 'GUL314'}, {'id': 'GUL315', 'label': 'GUL315'}, {'id': 'GUL316', 'label': 'GUL316'}, {'id': 'GUL317', 'label': 'GUL317'}, {'id': 'GUL318', 'label': 'GUL318'}, {'id': 'GUL319', 'label': 'GUL319'}, {'id': 'GUL320', 'label': 'GUL320'}, {'id': 'GUL321', 'label': 'GUL321'}, {'id': 'GUL322', 'label': 'GUL322'}, {'id': 'GUL323', 'label': 'GUL323'}, {'id': 'GUL324', 'label': 'GUL324'}, {'id': 'GUL325', 'label': 'GUL325'}, {'id': 'GUL326', 'label': 'GUL326'}, {'id': 'GUL327', 'label': 'GUL327'}, {'id': 'GUL328', 'label': 'GUL328'}, {'id': 'GUL329', 'label': 'GUL329'}, {'id': 'GUL330', 'label': 'GUL330'}, {'id': 'GUL331', 'label': 'GUL331'}, {'id': 'GUL332', 'label': 'GUL332'}, {'id': 'GUL333', 'label': 'GUL333'}, {'id': 'GUL334', 'label': 'GUL334'}, {'id': 'GUL335', 'label': 'GUL335'}, {'id': 'GUL336', 'label': 'GUL336'}, {'id': 'GUL337', 'label': 'GUL337'}, {'id': 'GUL338', 'label': 'GUL338'}, {'id': 'GUL339', 'label': 'GUL339'}, {'id': 'GUL340', 'label': 'GUL340'}, {'id': 'GUL341', 'label': 'GUL341'}, {'id': 'GUL342', 'label': 'GUL342'}, {'id': 'GUL343', 'label': 'GUL343'}, {'id': 'GUL344', 'label': 'GUL344'}, {'id': 'GUL345', 'label': 'GUL345'}, {'id': 'GUL346', 'label': 'GUL346'}, {'id': 'GUL347', 'label': 'GUL347'}, {'id': 'GUL348', 'label': 'GUL348'}, {'id': 'GUL349', 'label': 'GUL349'}, {'id': 'GUL350', 'label': 'GUL350'}, {'id': 'GUL351', 'label': 'GUL351'}, {'id': 'GUL352', 'label': 'GUL352'}, {'id': 'GUL353', 'label': 'GUL353'}, {'id': 'GUL354', 'label': 'GUL354'}, {'id': 'GUL355', 'label': 'GUL355'}, {'id': 'GUL356', 'label': 'GUL356'}, {'id': 'GUL357', 'label': 'GUL357'}, {'id': 'GUL358', 'label': 'GUL358'}, {'id': 'GUL359', 'label': 'GUL359'}, {'id': 'GUL360', 'label': 'GUL360'}, {'id': 'GUL361', 'label': 'GUL361'}, {'id': 'GUL362', 'label': 'GUL362'}, {'id': 'GUL363', 'label': 'GUL363'}, {'id': 'GUL364', 'label': 'GUL364'}, {'id': 'GUL365', 'label': 'GUL365'}, {'id': 'GUL366', 'label': 'GUL366'}, {'id': 'GUL367', 'label': 'GUL367'}, {'id': 'GUL368', 'label': 'GUL368'}, {'id': 'GUL369', 'label': 'GUL369'}, {'id': 'GUL370', 'label': 'GUL370'}, {'id': 'GUL371', 'label': 'GUL371'}, {'id': 'GUL372', 'label': 'GUL372'}, {'id': 'GUL373', 'label': 'GUL373'}, {'id': 'GUL374', 'label': 'GUL374'}, {'id': 'GUL375', 'label': 'GUL375'}, {'id': 'GUL376', 'label': 'GUL376'}, {'id': 'GUL377', 'label': 'GUL377'}, {'id': 'GUL378', 'label': 'GUL378'}, {'id': 'GUL379', 'label': 'GUL379'}, {'id': 'GUL380', 'label': 'GUL380'}, {'id': 'GUL381', 'label': 'GUL381'}, {'id': 'GUL382', 'label': 'GUL382'}, {'id': 'GUL383', 'label': 'GUL383'}, {'id': 'GUL384', 'label': 'GUL384'}, {'id': 'GUL385', 'label': 'GUL385'}, {'id': 'GUL386', 'label': 'GUL386'}, {'id': 'GUL387', 'label': 'GUL387'}, {'id': 'GUL388', 'label': 'GUL388'}, {'id': 'GUL389', 'label': 'GUL389'}, {'id': 'GUL390', 'label': 'GUL390'}, {'id': 'GUL391', 'label': 'GUL391'}, {'id': 'GUL392', 'label': 'GUL392'}, {'id': 'GUL393', 'label': 'GUL393'}, {'id': 'GUL394', 'label': 'GUL394'}, {'id': 'GUL395', 'label': 'GUL395'}, {'id': 'GUL396', 'label': 'GUL396'}, {'id': 'GUL397', 'label': 'GUL397'}, {'id': 'GUL398', 'label': 'GUL398'}, {'id': 'GUL399', 'label': 'GUL399'}, {'id': 'GUL400', 'label': 'GUL400'}, {'id': 'GUL401', 'label': 'GUL401'}, {'id': 'GUL402', 'label': 'GUL402'}, {'id': 'GUL403', 'label': 'GUL403'}, {'id': 'GUL404', 'label': 'GUL404'}, {'id': 'GUL405', 'label': 'GUL405'}, {'id': 'GUL406', 'label': 'GUL406'}, {'id': 'GUL407', 'label': 'GUL407'}, {'id': 'GUL408', 'label': 'GUL408'}, {'id': 'GUL409', 'label': 'GUL409'}, {'id': 'GUL410', 'label': 'GUL410'}, {'id': 'GUL411', 'label': 'GUL411'}, {'id': 'GUL412', 'label': 'GUL412'}, {'id': 'GUL413', 'label': 'GUL413'}, {'id': 'GUL414', 'label': 'GUL414'}, {'id': 'GUL415', 'label': 'GUL415'}, {'id': 'GUL416', 'label': 'GUL416'}, {'id': 'GUL417', 'label': 'GUL417'}, {'id': 'GUL418', 'label': 'GUL418'}, {'id': 'GUL419', 'label': 'GUL419'}, {'id': 'GUL420', 'label': 'GUL420'}, {'id': 'GUL421', 'label': 'GUL421'}, {'id': 'GUL422', 'label': 'GUL422'}, {'id': 'GUL423', 'label': 'GUL423'}, {'id': 'GUL424', 'label': 'GUL424'}, {'id': 'GUL425', 'label': 'GUL425'}, {'id': 'GUL426', 'label': 'GUL426'}, {'id': 'GUL427', 'label': 'GUL427'}, {'id': 'GUL428', 'label': 'GUL428'}, {'id': 'GUL429', 'label': 'GUL429'}, {'id': 'GUL430', 'label': 'GUL430'}, {'id': 'GUL431', 'label': 'GUL431'}, {'id': 'GUL432', 'label': 'GUL432'}, {'id': 'GUL433', 'label': 'GUL433'}, {'id': 'GUL434', 'label': 'GUL434'}, {'id': 'GUL435', 'label': 'GUL435'}, {'id': 'GUL436', 'label': 'GUL436'}, {'id': 'GUL437', 'label': 'GUL437'}, {'id': 'GUL438', 'label': 'GUL438'}, {'id': 'GUL439', 'label': 'GUL439'}, {'id': 'GUL440', 'label': 'GUL440'}, {'id': 'GUL441', 'label': 'GUL441'}, {'id': 'GUL442', 'label': 'GUL442'}, {'id': 'GUL443', 'label': 'GUL443'}, {'id': 'GUL444', 'label': 'GUL444'}, {'id': 'GUL445', 'label': 'GUL445'}, {'id': 'GUL446', 'label': 'GUL446'}, {'id': 'GUL447', 'label': 'GUL447'}, {'id': 'GUL448', 'label': 'GUL448'}, {'id': 'GUL449', 'label': 'GUL449'}, {'id': 'GUL450', 'label': 'GUL450'}, {'id': 'GUL451', 'label': 'GUL451'}, {'id': 'GUL452', 'label': 'GUL452'}, {'id': 'GUL453', 'label': 'GUL453'}, {'id': 'GUL454', 'label': 'GUL454'}, {'id': 'GUL455', 'label': 'GUL455'}, {'id': 'GUL456', 'label': 'GUL456'}, {'id': 'GUL457', 'label': 'GUL457'}, {'id': 'GUL458', 'label': 'GUL458'}, {'id': 'GUL459', 'label': 'GUL459'}, {'id': 'GUL460', 'label': 'GUL460'}, {'id': 'GUL461', 'label': 'GUL461'}, {'id': 'GUL462', 'label': 'GUL462'}, {'id': 'GUL463', 'label': 'GUL463'}, {'id': 'GUL464', 'label': 'GUL464'}, {'id': 'GUL465', 'label': 'GUL465'}, {'id': 'GUL466', 'label': 'GUL466'}, {'id': 'GUL467', 'label': 'GUL467'}, {'id': 'GUL468', 'label': 'GUL468'}, {'id': 'GUL469', 'label': 'GUL469'}, {'id': 'GUL470', 'label': 'GUL470'}, {'id': 'GUL471', 'label': 'GUL471'}, {'id': 'GUL472', 'label': 'GUL472'}, {'id': 'GUL473', 'label': 'GUL473'}, {'id': 'GUL474', 'label': 'GUL474'}, {'id': 'GUL475', 'label': 'GUL475'}, {'id': 'GUL476', 'label': 'GUL476'}, {'id': 'GUL477', 'label': 'GUL477'}, {'id': 'GUL478', 'label': 'GUL478'}, {'id': 'GUL479', 'label': 'GUL479'}, {'id': 'GUL480', 'label': 'GUL480'}, {'id': 'GUL481', 'label': 'GUL481'}, {'id': 'GUL482', 'label': 'GUL482'}, {'id': 'GUL483', 'label': 'GUL483'}, {'id': 'GUL484', 'label': 'GUL484'}, {'id': 'GUL485', 'label': 'GUL485'}, {'id': 'GUL486', 'label': 'GUL486'}, {'id': 'GUL487', 'label': 'GUL487'}, {'id': 'GUL488', 'label': 'GUL488'}, {'id': 'GUL489', 'label': 'GUL489'}, {'id': 'GUL490', 'label': 'GUL490'}, {'id': 'GUL491', 'label': 'GUL491'}, {'id': 'GUL492', 'label': 'GUL492'}, {'id': 'GUL493', 'label': 'GUL493'}, {'id': 'GUL494', 'label': 'GUL494'}, {'id': 'GUL495', 'label': 'GUL495'}, {'id': 'GUL496', 'label': 'GUL496'}, {'id': 'GUL497', 'label': 'GUL497'}, {'id': 'GUL498', 'label': 'GUL498'}, {'id': 'GUL499', 'label': 'GUL499'}, {'id': 'GUL500', 'label': 'GUL500'}]//, {'id': 'GUL501', 'label': 'GUL501'}, {'id': 'GUL502', 'label': 'GUL502'}, {'id': 'GUL503', 'label': 'GUL503'}, {'id': 'GUL504', 'label': 'GUL504'}, {'id': 'GUL505', 'label': 'GUL505'}, {'id': 'GUL506', 'label': 'GUL506'}, {'id': 'GUL507', 'label': 'GUL507'}, {'id': 'GUL508', 'label': 'GUL508'}, {'id': 'GUL509', 'label': 'GUL509'}, {'id': 'GUL510', 'label': 'GUL510'}, {'id': 'GUL511', 'label': 'GUL511'}, {'id': 'GUL512', 'label': 'GUL512'}, {'id': 'GUL513', 'label': 'GUL513'}, {'id': 'GUL514', 'label': 'GUL514'}, {'id': 'GUL515', 'label': 'GUL515'}, {'id': 'GUL516', 'label': 'GUL516'}, {'id': 'GUL517', 'label': 'GUL517'}, {'id': 'GUL518', 'label': 'GUL518'}, {'id': 'GUL519', 'label': 'GUL519'}, {'id': 'GUL520', 'label': 'GUL520'}, {'id': 'GUL521', 'label': 'GUL521'}, {'id': 'GUL522', 'label': 'GUL522'}, {'id': 'GUL523', 'label': 'GUL523'}, {'id': 'GUL524', 'label': 'GUL524'}, {'id': 'GUL525', 'label': 'GUL525'}, {'id': 'GUL526', 'label': 'GUL526'}, {'id': 'GUL527', 'label': 'GUL527'}, {'id': 'GUL528', 'label': 'GUL528'}, {'id': 'GUL529', 'label': 'GUL529'}, {'id': 'GUL530', 'label': 'GUL530'}, {'id': 'GUL531', 'label': 'GUL531'}, {'id': 'GUL532', 'label': 'GUL532'}, {'id': 'GUL533', 'label': 'GUL533'}, {'id': 'GUL534', 'label': 'GUL534'}, {'id': 'GUL535', 'label': 'GUL535'}, {'id': 'GUL536', 'label': 'GUL536'}, {'id': 'GUL537', 'label': 'GUL537'}, {'id': 'GUL538', 'label': 'GUL538'}, {'id': 'GUL539', 'label': 'GUL539'}, {'id': 'GUL540', 'label': 'GUL540'}, {'id': 'GUL541', 'label': 'GUL541'}, {'id': 'GUL542', 'label': 'GUL542'}, {'id': 'GUL543', 'label': 'GUL543'}, {'id': 'GUL544', 'label': 'GUL544'}, {'id': 'GUL545', 'label': 'GUL545'}, {'id': 'GUL546', 'label': 'GUL546'}, {'id': 'GUL547', 'label': 'GUL547'}, {'id': 'GUL548', 'label': 'GUL548'}, {'id': 'GUL549', 'label': 'GUL549'}, {'id': 'GUL550', 'label': 'GUL550'}, {'id': 'GUL551', 'label': 'GUL551'}, {'id': 'GUL552', 'label': 'GUL552'}, {'id': 'GUL553', 'label': 'GUL553'}, {'id': 'GUL554', 'label': 'GUL554'}, {'id': 'GUL555', 'label': 'GUL555'}, {'id': 'GUL556', 'label': 'GUL556'}, {'id': 'GUL557', 'label': 'GUL557'}, {'id': 'GUL558', 'label': 'GUL558'}, {'id': 'GUL559', 'label': 'GUL559'}, {'id': 'GUL560', 'label': 'GUL560'}, {'id': 'GUL561', 'label': 'GUL561'}, {'id': 'GUL562', 'label': 'GUL562'}, {'id': 'GUL563', 'label': 'GUL563'}, {'id': 'GUL564', 'label': 'GUL564'}, {'id': 'GUL565', 'label': 'GUL565'}, {'id': 'GUL566', 'label': 'GUL566'}, {'id': 'GUL567', 'label': 'GUL567'}, {'id': 'GUL568', 'label': 'GUL568'}, {'id': 'GUL569', 'label': 'GUL569'}, {'id': 'GUL570', 'label': 'GUL570'}, {'id': 'GUL571', 'label': 'GUL571'}, {'id': 'GUL572', 'label': 'GUL572'}, {'id': 'GUL573', 'label': 'GUL573'}, {'id': 'GUL574', 'label': 'GUL574'}, {'id': 'GUL575', 'label': 'GUL575'}, {'id': 'GUL576', 'label': 'GUL576'}, {'id': 'GUL577', 'label': 'GUL577'}, {'id': 'GUL578', 'label': 'GUL578'}, {'id': 'GUL579', 'label': 'GUL579'}, {'id': 'GUL580', 'label': 'GUL580'}, {'id': 'GUL581', 'label': 'GUL581'}, {'id': 'GUL582', 'label': 'GUL582'}, {'id': 'GUL583', 'label': 'GUL583'}, {'id': 'GUL584', 'label': 'GUL584'}, {'id': 'GUL585', 'label': 'GUL585'}, {'id': 'GUL586', 'label': 'GUL586'}, {'id': 'GUL587', 'label': 'GUL587'}, {'id': 'GUL588', 'label': 'GUL588'}, {'id': 'GUL589', 'label': 'GUL589'}, {'id': 'GUL590', 'label': 'GUL590'}, {'id': 'GUL591', 'label': 'GUL591'}, {'id': 'GUL592', 'label': 'GUL592'}, {'id': 'GUL593', 'label': 'GUL593'}, {'id': 'GUL594', 'label': 'GUL594'}, {'id': 'GUL595', 'label': 'GUL595'}, {'id': 'GUL596', 'label': 'GUL596'}, {'id': 'GUL597', 'label': 'GUL597'}, {'id': 'GUL598', 'label': 'GUL598'}, {'id': 'GUL599', 'label': 'GUL599'}, {'id': 'GUL600', 'label': 'GUL600'}, {'id': 'GUL601', 'label': 'GUL601'}, {'id': 'GUL602', 'label': 'GUL602'}, {'id': 'GUL603', 'label': 'GUL603'}, {'id': 'GUL604', 'label': 'GUL604'}, {'id': 'GUL605', 'label': 'GUL605'}, {'id': 'GUL606', 'label': 'GUL606'}, {'id': 'GUL607', 'label': 'GUL607'}, {'id': 'GUL608', 'label': 'GUL608'}, {'id': 'GUL609', 'label': 'GUL609'}, {'id': 'GUL610', 'label': 'GUL610'}, {'id': 'GUL611', 'label': 'GUL611'}, {'id': 'GUL612', 'label': 'GUL612'}, {'id': 'GUL613', 'label': 'GUL613'}, {'id': 'GUL614', 'label': 'GUL614'}, {'id': 'GUL615', 'label': 'GUL615'}, {'id': 'GUL616', 'label': 'GUL616'}, {'id': 'GUL617', 'label': 'GUL617'}, {'id': 'GUL618', 'label': 'GUL618'}, {'id': 'GUL619', 'label': 'GUL619'}, {'id': 'GUL620', 'label': 'GUL620'}, {'id': 'GUL621', 'label': 'GUL621'}, {'id': 'GUL622', 'label': 'GUL622'}, {'id': 'GUL623', 'label': 'GUL623'}, {'id': 'GUL624', 'label': 'GUL624'}, {'id': 'GUL625', 'label': 'GUL625'}, {'id': 'GUL626', 'label': 'GUL626'}, {'id': 'GUL627', 'label': 'GUL627'}, {'id': 'GUL628', 'label': 'GUL628'}, {'id': 'GUL629', 'label': 'GUL629'}, {'id': 'GUL630', 'label': 'GUL630'}, {'id': 'GUL631', 'label': 'GUL631'}, {'id': 'GUL632', 'label': 'GUL632'}, {'id': 'GUL633', 'label': 'GUL633'}, {'id': 'GUL634', 'label': 'GUL634'}, {'id': 'GUL635', 'label': 'GUL635'}, {'id': 'GUL636', 'label': 'GUL636'}, {'id': 'GUL637', 'label': 'GUL637'}, {'id': 'GUL638', 'label': 'GUL638'}, {'id': 'GUL639', 'label': 'GUL639'}, {'id': 'GUL640', 'label': 'GUL640'}, {'id': 'GUL641', 'label': 'GUL641'}, {'id': 'GUL642', 'label': 'GUL642'}, {'id': 'GUL643', 'label': 'GUL643'}, {'id': 'GUL644', 'label': 'GUL644'}, {'id': 'GUL645', 'label': 'GUL645'}, {'id': 'GUL646', 'label': 'GUL646'}, {'id': 'GUL647', 'label': 'GUL647'}, {'id': 'GUL648', 'label': 'GUL648'}, {'id': 'GUL649', 'label': 'GUL649'}, {'id': 'GUL650', 'label': 'GUL650'}, {'id': 'GUL651', 'label': 'GUL651'}, {'id': 'GUL652', 'label': 'GUL652'}, {'id': 'GUL653', 'label': 'GUL653'}, {'id': 'GUL654', 'label': 'GUL654'}, {'id': 'GUL655', 'label': 'GUL655'}, {'id': 'GUL656', 'label': 'GUL656'}, {'id': 'GUL657', 'label': 'GUL657'}, {'id': 'GUL658', 'label': 'GUL658'}, {'id': 'GUL659', 'label': 'GUL659'}, {'id': 'GUL660', 'label': 'GUL660'}, {'id': 'GUL661', 'label': 'GUL661'}, {'id': 'GUL662', 'label': 'GUL662'}, {'id': 'GUL663', 'label': 'GUL663'}, {'id': 'GUL664', 'label': 'GUL664'}, {'id': 'GUL665', 'label': 'GUL665'}, {'id': 'GUL666', 'label': 'GUL666'}, {'id': 'GUL667', 'label': 'GUL667'}, {'id': 'GUL668', 'label': 'GUL668'}, {'id': 'GUL669', 'label': 'GUL669'}, {'id': 'GUL670', 'label': 'GUL670'}, {'id': 'GUL671', 'label': 'GUL671'}, {'id': 'GUL672', 'label': 'GUL672'}, {'id': 'GUL673', 'label': 'GUL673'}, {'id': 'GUL674', 'label': 'GUL674'}, {'id': 'GUL675', 'label': 'GUL675'}, {'id': 'GUL676', 'label': 'GUL676'}, {'id': 'GUL677', 'label': 'GUL677'}, {'id': 'GUL678', 'label': 'GUL678'}, {'id': 'GUL679', 'label': 'GUL679'}, {'id': 'GUL680', 'label': 'GUL680'}, {'id': 'GUL681', 'label': 'GUL681'}, {'id': 'GUL682', 'label': 'GUL682'}, {'id': 'GUL683', 'label': 'GUL683'}, {'id': 'GUL684', 'label': 'GUL684'}, {'id': 'GUL685', 'label': 'GUL685'}, {'id': 'GUL686', 'label': 'GUL686'}, {'id': 'GUL687', 'label': 'GUL687'}, {'id': 'GUL688', 'label': 'GUL688'}, {'id': 'GUL689', 'label': 'GUL689'}, {'id': 'GUL690', 'label': 'GUL690'}, {'id': 'GUL691', 'label': 'GUL691'}, {'id': 'GUL692', 'label': 'GUL692'}, {'id': 'GUL693', 'label': 'GUL693'}, {'id': 'GUL694', 'label': 'GUL694'}, {'id': 'GUL695', 'label': 'GUL695'}, {'id': 'GUL696', 'label': 'GUL696'}, {'id': 'GUL697', 'label': 'GUL697'}, {'id': 'GUL698', 'label': 'GUL698'}, {'id': 'GUL699', 'label': 'GUL699'}, {'id': 'GUL700', 'label': 'GUL700'}, {'id': 'GUL701', 'label': 'GUL701'}, {'id': 'GUL702', 'label': 'GUL702'}, {'id': 'GUL703', 'label': 'GUL703'}, {'id': 'GUL704', 'label': 'GUL704'}, {'id': 'GUL705', 'label': 'GUL705'}, {'id': 'GUL706', 'label': 'GUL706'}, {'id': 'GUL707', 'label': 'GUL707'}, {'id': 'GUL708', 'label': 'GUL708'}, {'id': 'GUL709', 'label': 'GUL709'}, {'id': 'GUL710', 'label': 'GUL710'}, {'id': 'GUL711', 'label': 'GUL711'}, {'id': 'GUL712', 'label': 'GUL712'}, {'id': 'GUL713', 'label': 'GUL713'}, {'id': 'GUL714', 'label': 'GUL714'}, {'id': 'GUL715', 'label': 'GUL715'}, {'id': 'GUL716', 'label': 'GUL716'}, {'id': 'GUL717', 'label': 'GUL717'}, {'id': 'GUL718', 'label': 'GUL718'}, {'id': 'GUL719', 'label': 'GUL719'}, {'id': 'GUL720', 'label': 'GUL720'}, {'id': 'GUL721', 'label': 'GUL721'}, {'id': 'GUL722', 'label': 'GUL722'}, {'id': 'GUL723', 'label': 'GUL723'}, {'id': 'GUL724', 'label': 'GUL724'}, {'id': 'GUL725', 'label': 'GUL725'}, {'id': 'GUL726', 'label': 'GUL726'}, {'id': 'GUL727', 'label': 'GUL727'}, {'id': 'GUL728', 'label': 'GUL728'}, {'id': 'GUL729', 'label': 'GUL729'}, {'id': 'GUL730', 'label': 'GUL730'}, {'id': 'GUL731', 'label': 'GUL731'}, {'id': 'GUL732', 'label': 'GUL732'}, {'id': 'GUL733', 'label': 'GUL733'}, {'id': 'GUL734', 'label': 'GUL734'}, {'id': 'GUL735', 'label': 'GUL735'}, {'id': 'GUL736', 'label': 'GUL736'}, {'id': 'GUL737', 'label': 'GUL737'}, {'id': 'GUL738', 'label': 'GUL738'}, {'id': 'GUL739', 'label': 'GUL739'}, {'id': 'GUL740', 'label': 'GUL740'}, {'id': 'GUL741', 'label': 'GUL741'}, {'id': 'GUL742', 'label': 'GUL742'}, {'id': 'GUL743', 'label': 'GUL743'}, {'id': 'GUL744', 'label': 'GUL744'}, {'id': 'GUL745', 'label': 'GUL745'}, {'id': 'GUL746', 'label': 'GUL746'}, {'id': 'GUL747', 'label': 'GUL747'}, {'id': 'GUL748', 'label': 'GUL748'}, {'id': 'GUL749', 'label': 'GUL749'}, {'id': 'GUL750', 'label': 'GUL750'}, {'id': 'GUL751', 'label': 'GUL751'}, {'id': 'GUL752', 'label': 'GUL752'}, {'id': 'GUL753', 'label': 'GUL753'}, {'id': 'GUL754', 'label': 'GUL754'}, {'id': 'GUL755', 'label': 'GUL755'}, {'id': 'GUL756', 'label': 'GUL756'}, {'id': 'GUL757', 'label': 'GUL757'}, {'id': 'GUL758', 'label': 'GUL758'}, {'id': 'GUL759', 'label': 'GUL759'}, {'id': 'GUL760', 'label': 'GUL760'}, {'id': 'GUL761', 'label': 'GUL761'}, {'id': 'GUL762', 'label': 'GUL762'}, {'id': 'GUL763', 'label': 'GUL763'}, {'id': 'GUL764', 'label': 'GUL764'}, {'id': 'GUL765', 'label': 'GUL765'}, {'id': 'GUL766', 'label': 'GUL766'}, {'id': 'GUL767', 'label': 'GUL767'}, {'id': 'GUL768', 'label': 'GUL768'}, {'id': 'GUL769', 'label': 'GUL769'}, {'id': 'GUL770', 'label': 'GUL770'}, {'id': 'GUL771', 'label': 'GUL771'}, {'id': 'GUL772', 'label': 'GUL772'}, {'id': 'GUL773', 'label': 'GUL773'}, {'id': 'GUL774', 'label': 'GUL774'}, {'id': 'GUL775', 'label': 'GUL775'}, {'id': 'GUL776', 'label': 'GUL776'}, {'id': 'GUL777', 'label': 'GUL777'}, {'id': 'GUL778', 'label': 'GUL778'}, {'id': 'GUL779', 'label': 'GUL779'}, {'id': 'GUL780', 'label': 'GUL780'}, {'id': 'GUL781', 'label': 'GUL781'}, {'id': 'GUL782', 'label': 'GUL782'}, {'id': 'GUL783', 'label': 'GUL783'}, {'id': 'GUL784', 'label': 'GUL784'}, {'id': 'GUL785', 'label': 'GUL785'}, {'id': 'GUL786', 'label': 'GUL786'}, {'id': 'GUL787', 'label': 'GUL787'}, {'id': 'GUL788', 'label': 'GUL788'}, {'id': 'GUL789', 'label': 'GUL789'}, {'id': 'GUL790', 'label': 'GUL790'}, {'id': 'GUL791', 'label': 'GUL791'}, {'id': 'GUL792', 'label': 'GUL792'}, {'id': 'GUL793', 'label': 'GUL793'}, {'id': 'GUL794', 'label': 'GUL794'}, {'id': 'GUL795', 'label': 'GUL795'}, {'id': 'GUL796', 'label': 'GUL796'}, {'id': 'GUL797', 'label': 'GUL797'}, {'id': 'GUL798', 'label': 'GUL798'}, {'id': 'GUL799', 'label': 'GUL799'}, {'id': 'GUL800', 'label': 'GUL800'}, {'id': 'GUL801', 'label': 'GUL801'}, {'id': 'GUL802', 'label': 'GUL802'}, {'id': 'GUL803', 'label': 'GUL803'}, {'id': 'GUL804', 'label': 'GUL804'}, {'id': 'GUL805', 'label': 'GUL805'}, {'id': 'GUL806', 'label': 'GUL806'}, {'id': 'GUL807', 'label': 'GUL807'}, {'id': 'GUL808', 'label': 'GUL808'}, {'id': 'GUL809', 'label': 'GUL809'}, {'id': 'GUL810', 'label': 'GUL810'}, {'id': 'GUL811', 'label': 'GUL811'}, {'id': 'GUL812', 'label': 'GUL812'}, {'id': 'GUL813', 'label': 'GUL813'}, {'id': 'GUL814', 'label': 'GUL814'}, {'id': 'GUL815', 'label': 'GUL815'}, {'id': 'GUL816', 'label': 'GUL816'}, {'id': 'GUL817', 'label': 'GUL817'}, {'id': 'GUL818', 'label': 'GUL818'}, {'id': 'GUL819', 'label': 'GUL819'}, {'id': 'GUL820', 'label': 'GUL820'}, {'id': 'GUL821', 'label': 'GUL821'}, {'id': 'GUL822', 'label': 'GUL822'}, {'id': 'GUL823', 'label': 'GUL823'}, {'id': 'GUL824', 'label': 'GUL824'}, {'id': 'GUL825', 'label': 'GUL825'}, {'id': 'GUL826', 'label': 'GUL826'}, {'id': 'GUL827', 'label': 'GUL827'}, {'id': 'GUL828', 'label': 'GUL828'}, {'id': 'GUL829', 'label': 'GUL829'}, {'id': 'GUL830', 'label': 'GUL830'}, {'id': 'GUL831', 'label': 'GUL831'}, {'id': 'GUL832', 'label': 'GUL832'}, {'id': 'GUL833', 'label': 'GUL833'}, {'id': 'GUL834', 'label': 'GUL834'}, {'id': 'GUL835', 'label': 'GUL835'}, {'id': 'GUL836', 'label': 'GUL836'}, {'id': 'GUL837', 'label': 'GUL837'}, {'id': 'GUL838', 'label': 'GUL838'}, {'id': 'GUL839', 'label': 'GUL839'}, {'id': 'GUL840', 'label': 'GUL840'}, {'id': 'GUL841', 'label': 'GUL841'}, {'id': 'GUL842', 'label': 'GUL842'}, {'id': 'GUL843', 'label': 'GUL843'}, {'id': 'GUL844', 'label': 'GUL844'}, {'id': 'GUL845', 'label': 'GUL845'}, {'id': 'GUL846', 'label': 'GUL846'}, {'id': 'GUL847', 'label': 'GUL847'}, {'id': 'GUL848', 'label': 'GUL848'}, {'id': 'GUL849', 'label': 'GUL849'}, {'id': 'GUL850', 'label': 'GUL850'}, {'id': 'GUL851', 'label': 'GUL851'}, {'id': 'GUL852', 'label': 'GUL852'}, {'id': 'GUL853', 'label': 'GUL853'}, {'id': 'GUL854', 'label': 'GUL854'}, {'id': 'GUL855', 'label': 'GUL855'}, {'id': 'GUL856', 'label': 'GUL856'}, {'id': 'GUL857', 'label': 'GUL857'}, {'id': 'GUL858', 'label': 'GUL858'}, {'id': 'GUL859', 'label': 'GUL859'}, {'id': 'GUL860', 'label': 'GUL860'}, {'id': 'GUL861', 'label': 'GUL861'}, {'id': 'GUL862', 'label': 'GUL862'}, {'id': 'GUL863', 'label': 'GUL863'}, {'id': 'GUL864', 'label': 'GUL864'}, {'id': 'GUL865', 'label': 'GUL865'}, {'id': 'GUL866', 'label': 'GUL866'}, {'id': 'GUL867', 'label': 'GUL867'}, {'id': 'GUL868', 'label': 'GUL868'}, {'id': 'GUL869', 'label': 'GUL869'}, {'id': 'GUL870', 'label': 'GUL870'}, {'id': 'GUL871', 'label': 'GUL871'}, {'id': 'GUL872', 'label': 'GUL872'}, {'id': 'GUL873', 'label': 'GUL873'}, {'id': 'GUL874', 'label': 'GUL874'}, {'id': 'GUL875', 'label': 'GUL875'}, {'id': 'GUL876', 'label': 'GUL876'}, {'id': 'GUL877', 'label': 'GUL877'}, {'id': 'GUL878', 'label': 'GUL878'}, {'id': 'GUL879', 'label': 'GUL879'}, {'id': 'GUL880', 'label': 'GUL880'}, {'id': 'GUL881', 'label': 'GUL881'}, {'id': 'GUL882', 'label': 'GUL882'}, {'id': 'GUL883', 'label': 'GUL883'}, {'id': 'GUL884', 'label': 'GUL884'}, {'id': 'GUL885', 'label': 'GUL885'}, {'id': 'GUL886', 'label': 'GUL886'}, {'id': 'GUL887', 'label': 'GUL887'}, {'id': 'GUL888', 'label': 'GUL888'}, {'id': 'GUL889', 'label': 'GUL889'}, {'id': 'GUL890', 'label': 'GUL890'}, {'id': 'GUL891', 'label': 'GUL891'}, {'id': 'GUL892', 'label': 'GUL892'}, {'id': 'GUL893', 'label': 'GUL893'}, {'id': 'GUL894', 'label': 'GUL894'}, {'id': 'GUL895', 'label': 'GUL895'}, {'id': 'GUL896', 'label': 'GUL896'}, {'id': 'GUL897', 'label': 'GUL897'}, {'id': 'GUL898', 'label': 'GUL898'}, {'id': 'GUL899', 'label': 'GUL899'}, {'id': 'GUL900', 'label': 'GUL900'}, {'id': 'GUL901', 'label': 'GUL901'}, {'id': 'GUL902', 'label': 'GUL902'}, {'id': 'GUL903', 'label': 'GUL903'}, {'id': 'GUL904', 'label': 'GUL904'}, {'id': 'GUL905', 'label': 'GUL905'}, {'id': 'GUL906', 'label': 'GUL906'}, {'id': 'GUL907', 'label': 'GUL907'}, {'id': 'GUL908', 'label': 'GUL908'}, {'id': 'GUL909', 'label': 'GUL909'}, {'id': 'GUL910', 'label': 'GUL910'}, {'id': 'GUL911', 'label': 'GUL911'}, {'id': 'GUL912', 'label': 'GUL912'}, {'id': 'GUL913', 'label': 'GUL913'}, {'id': 'GUL914', 'label': 'GUL914'}, {'id': 'GUL915', 'label': 'GUL915'}, {'id': 'GUL916', 'label': 'GUL916'}, {'id': 'GUL917', 'label': 'GUL917'}, {'id': 'GUL918', 'label': 'GUL918'}, {'id': 'GUL919', 'label': 'GUL919'}, {'id': 'GUL920', 'label': 'GUL920'}, {'id': 'GUL921', 'label': 'GUL921'}, {'id': 'GUL922', 'label': 'GUL922'}, {'id': 'GUL923', 'label': 'GUL923'}, {'id': 'GUL924', 'label': 'GUL924'}, {'id': 'GUL925', 'label': 'GUL925'}, {'id': 'GUL926', 'label': 'GUL926'}, {'id': 'GUL927', 'label': 'GUL927'}, {'id': 'GUL928', 'label': 'GUL928'}, {'id': 'GUL929', 'label': 'GUL929'}, {'id': 'GUL930', 'label': 'GUL930'}, {'id': 'GUL931', 'label': 'GUL931'}, {'id': 'GUL932', 'label': 'GUL932'}, {'id': 'GUL933', 'label': 'GUL933'}, {'id': 'GUL934', 'label': 'GUL934'}, {'id': 'GUL935', 'label': 'GUL935'}, {'id': 'GUL936', 'label': 'GUL936'}, {'id': 'GUL937', 'label': 'GUL937'}, {'id': 'GUL938', 'label': 'GUL938'}, {'id': 'GUL939', 'label': 'GUL939'}, {'id': 'GUL940', 'label': 'GUL940'}, {'id': 'GUL941', 'label': 'GUL941'}, {'id': 'GUL942', 'label': 'GUL942'}, {'id': 'GUL943', 'label': 'GUL943'}, {'id': 'GUL944', 'label': 'GUL944'}, {'id': 'GUL945', 'label': 'GUL945'}, {'id': 'GUL946', 'label': 'GUL946'}, {'id': 'GUL947', 'label': 'GUL947'}, {'id': 'GUL948', 'label': 'GUL948'}, {'id': 'GUL949', 'label': 'GUL949'}, {'id': 'GUL950', 'label': 'GUL950'}, {'id': 'GUL951', 'label': 'GUL951'}, {'id': 'GUL952', 'label': 'GUL952'}, {'id': 'GUL953', 'label': 'GUL953'}, {'id': 'GUL954', 'label': 'GUL954'}, {'id': 'GUL955', 'label': 'GUL955'}, {'id': 'GUL956', 'label': 'GUL956'}, {'id': 'GUL957', 'label': 'GUL957'}, {'id': 'GUL958', 'label': 'GUL958'}, {'id': 'GUL959', 'label': 'GUL959'}, {'id': 'GUL960', 'label': 'GUL960'}, {'id': 'GUL961', 'label': 'GUL961'}, {'id': 'GUL962', 'label': 'GUL962'}, {'id': 'GUL963', 'label': 'GUL963'}, {'id': 'GUL964', 'label': 'GUL964'}, {'id': 'GUL965', 'label': 'GUL965'}, {'id': 'GUL966', 'label': 'GUL966'}, {'id': 'GUL967', 'label': 'GUL967'}, {'id': 'GUL968', 'label': 'GUL968'}, {'id': 'GUL969', 'label': 'GUL969'}, {'id': 'GUL970', 'label': 'GUL970'}, {'id': 'GUL971', 'label': 'GUL971'}, {'id': 'GUL972', 'label': 'GUL972'}, {'id': 'GUL973', 'label': 'GUL973'}, {'id': 'GUL974', 'label': 'GUL974'}, {'id': 'GUL975', 'label': 'GUL975'}, {'id': 'GUL976', 'label': 'GUL976'}, {'id': 'GUL977', 'label': 'GUL977'}, {'id': 'GUL978', 'label': 'GUL978'}, {'id': 'GUL979', 'label': 'GUL979'}, {'id': 'GUL980', 'label': 'GUL980'}, {'id': 'GUL981', 'label': 'GUL981'}, {'id': 'GUL982', 'label': 'GUL982'}, {'id': 'GUL983', 'label': 'GUL983'}, {'id': 'GUL984', 'label': 'GUL984'}, {'id': 'GUL985', 'label': 'GUL985'}, {'id': 'GUL986', 'label': 'GUL986'}, {'id': 'GUL987', 'label': 'GUL987'}, {'id': 'GUL988', 'label': 'GUL988'}, {'id': 'GUL989', 'label': 'GUL989'}, {'id': 'GUL990', 'label': 'GUL990'}, {'id': 'GUL991', 'label': 'GUL991'}, {'id': 'GUL992', 'label': 'GUL992'}, {'id': 'GUL993', 'label': 'GUL993'}, {'id': 'GUL994', 'label': 'GUL994'}, {'id': 'GUL995', 'label': 'GUL995'}, {'id': 'GUL996', 'label': 'GUL996'}, {'id': 'GUL997', 'label': 'GUL997'}, {'id': 'GUL998', 'label': 'GUL998'}, {'id': 'GUL999', 'label': 'GUL999'}, {'id': 'GUL1000', 'label': 'GUL1000'}]
                            };
                        }

                        if(row === 8){
                            cellProperties.readOnly = true;
                        }

                        if (col === 0) {
                            
                            cellProperties.readOnly = true;
                            cellProperties.className = "htCenter htMiddle";
                        }

                        return cellProperties;
                    },
                    afterChange: function (changes, source) {
                        if (!changes) {
                            return;
                        }

                        $timeout(function(){
                          $scope.hasError.boolean= true;
                        });

                        $.each(changes, function (index, element) {
                            data_strategies[element[0]][element[1]] = element[3];
                            //element[4] value before changement
                        });
                        
                     },
                     afterSelection: function (r, c, r2, c2) {
                        if(r == 6 && c !=0){
                            $scope.warning="";
                            $scope.success="";
                            row=r;
                            col=c;
                            $scope.onto=null;
                            Dataset.ontologies({},{'stringToDict': true, 'string':data_strategies[row][col]}).$promise.then(function(data){
                                $scope.value=data[0];
                            });
                            openOntology();
                        }
                    },
                },

                hot1;
                hot1 = new Handsontable(container, settings);
                hot1.render();
        
            };
            
            function table_list(){
                data1 = data_lists,
                container = document.getElementById('excelTable'),
                settings = {
                    data:data1,
                    width: 1100,
                    height: 320,
                    stretchH: 'all',
                    rowHeights: 30, 
                    colWidths: [350, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75],
                    rowHeaders:true,
                    colHeaders:true,
                    maxRows:9,
                    maxCols:1001,
                    wordWrap:false,
                    renderer: 'html',
                    fixedRowsTop: 0,
                    fixedColumnsLeft: 1,
                    //autoRowSize:true,
                    manualRowResize : false,
                    manualColumnResize: true,
                    manualRowResize: true,
                    allowEmpty: true,
                    cells: function (row, col, prop) {
                        var cellProperties = {};

                        if (row === 0) {   
                            cellProperties.readOnly = true; 
                            cellProperties.className = "htCenter htMiddle";
                        }
                        if (row == 5){

                            cellProperties.renderer = customDropdownRenderer;
                            cellProperties.editor = "chosen";
                            cellProperties.width = 150;
                            cellProperties.chosenOptions ={
                                multiple: false,
                                data:  [{'id':'Yes', 'label':'Yes'},{'id':'No', 'label':'No'}]
                            };
                        }

                        if (row === 7){
                            cellProperties.renderer = customDropdownRenderer;
                            cellProperties.editor = "chosen";
                            cellProperties.width = 150;
                            cellProperties.chosenOptions ={
                                multiple: false,
                                data:  [{'id':'Yes', 'label':'Yes'},{'id':'No', 'label':'No'}]
                            };
                        }

                        if (col === 0) {
                            cellProperties.readOnly = true;
                            cellProperties.className = "htCenter htMiddle";
                        }
                        
                        return cellProperties;
                    },
                    afterChange: function (changes, source) {
                        if (!changes) {
                            return;
                        }

                        $timeout(function(){
                          $scope.hasError.boolean= true;
                        });

                        $.each(changes, function (index, element) {
                            data_lists[element[0]][element[1]] = element[3];
                            //element[4] value before changement
                        });
                    },
                    afterSelection: function (r, c, r2, c2) {
                        if(r == 4 && c !=0){
                            $scope.warning="";
                            $scope.success="";
                            row=r;
                            col=c;
                            $scope.onto=null;
                            Dataset.ontologies({},{'stringToDict': true, 'string':data_lists[row][col]}).$promise.then(function(data){
                                $scope.value=data[0];
                            });
                            openOntology();
                        }

                        if(r == 5 && c !=0){
                            $scope.warning="";
                            $scope.success="";
                            row=r
                            col=c
                            $scope.database=data_lists[row][col]
                            openDatabase(r,c);
                        }
                    },
                },

                hot1;
                hot1 = new Handsontable(container, settings);
                hot1.render();

            };

            function customDropdownRenderer(instance, td, row, col, prop, value, cellProperties) {
                var selectedId;
                var optionsList = cellProperties.chosenOptions.data;

                if(typeof optionsList === "undefined" || typeof optionsList.length === "undefined" || !optionsList.length) {
                    Handsontable.renderers.TextRenderer.apply(this, arguments);
                    // Handsontable.TextCell.renderer(instance, td, row, col, prop, value, cellProperties);
                    return td;
                }

                var values = (value + "").split(",");
                value = [];

                for (var index = 0; index < optionsList.length; index++) {

                    if (values.indexOf(optionsList[index].id + "") > -1) {
                        selectedId = optionsList[index].id;
                        value.push(optionsList[index].label);
                    }
                }

                cellProperties.className ="htCenter htMiddle";
                Handsontable.renderers.TextRenderer.apply(this, arguments);

                return td;
            };

            function rowOntologyRenderer(instance, td, row, col, prop, value, cellProperties) {
                Handsontable.renderers.TextRenderer.apply(this, arguments);
                    td.style.color = '#333';
            };

            $scope.onViewOntologyChange = function() {
                $scope.viewOntology=!$scope.viewOntology;
                $scope.warning="";
                $scope.success="";
            };

            $scope.isValueEmpty = function(){
               return Object.keys($scope.value).length === 0;
            };

            $scope.removeOntoDatabaseSelected = function(){
                $scope.ontoDatabaseSelected.value=""
            };

            $scope.onDatabaseChange= function(){
                $scope.onto=null;
                $scope.selectOnto="";
                $scope.search_result=[];
            };

            $scope.get_onto = function() {
                $scope.onto=null;
                $timeout(function(){

                    $scope.warning="";
                    $scope.success="";
                    var val = document.getElementById('organism_vivo').value;
                    Dataset.ontologies({},{'database':$scope.ontoDatabaseSelected.value.id,'search':document.getElementById('organism_vivo').value}).$promise.then(function(data){
                        data.map(function(item){
                            $scope.search_result = [];
                            Object.keys(item).map(function(key, index) {
                                $scope.search_result.push(item[key]);
                            });
                        });
                    });
                });
            };
            
            function openOntology(){
                if(!$scope.dialog) {
                    $scope.dialog = ngDialog.open({
                        template: 'Ontology',
                        className: 'ngdialog-theme-flat ngdialog-theme-custom',
                        scope: $scope
                    });
                }

                $scope.dialog.closePromise.then(function(data) {

                    Dataset.ontologies({},{'dictToString': true, 'dico': $scope.value}).$promise.then(function(data){
                        if(whichTableView=="project"){
                            data_projects[row][col]=data[0];
                            hot1.setDataAtCell(row, col, data_projects[row][col]);
                        }

                        else if(whichTableView=="strategy"){
                            data_strategies[row][col]=data[0];
                            hot1.setDataAtCell(row, col, data_strategies[row][col]);
                        }

                        else{
                            data_lists[row][col]=data[0];
                            hot1.setDataAtCell(row, col, data_lists[row][col]);
                        }
                    });
                    $scope.dialog = null;
                    $scope.warning="";
                    $scope.success="";
                    $scope.value=null;
                    $scope.onto=null;
                    $scope.ontoDatabaseSelected.value="";
                    $scope.viewOntology = true;
                });
            };

            $scope.selected_tissue = function(item, model,label){
                $scope.onto = item;
            };

            $scope.addOntology = function(){
                $scope.warning="";
                $scope.success="";

                if($scope.onto == null){
                    return $scope.warning="Select a result from search before adding";
                }
                if(!($scope.ontoDatabaseSelected.value.id in $scope.value)){ // if our object has already a key (i.e. NCBITaxon) return false
                        $scope.value[$scope.ontoDatabaseSelected.value.id] = [];
                        $scope.value[$scope.ontoDatabaseSelected.value.id].push($scope.onto.prefLabel);
                        $scope.success=$scope.onto.prefLabel+" Added to your list";
                        document.getElementById('organism_vivo').value="";
                        $scope.onto=null;
                }
                else{
                    
                    if($scope.value[$scope.ontoDatabaseSelected.value.id].includes($scope.onto.prefLabel)){
                        $scope.warning=$scope.onto.prefLabel+' ontology is already in your list';
                        $scope.onto=null;
                    }
                    else{
                        $scope.value[$scope.ontoDatabaseSelected.value.id].push($scope.onto.prefLabel);
                        $scope.success=$scope.onto.prefLabel+" Added to your list";
                        document.getElementById('organism_vivo').value="";
                        $scope.onto=null;
                    }
                }
            }

            Array.prototype.remove= function(){
                var what, a= arguments, L= a.length, ax;
                while(L && this.length){
                    what= a[--L];
                    while((ax= this.indexOf(what))!= -1){
                        this.splice(ax, 1);
                    }
                }
                return this;
            };

            $scope.removeOntology = function(database,term){
                if($scope.value[database].length == 1){
                    delete $scope.value[database];
                }
                else{
                    var newterm = $scope.value[database].remove(term);
                    $scope.value[database] = newterm; 
                }
            };

            $scope.showReport = function(){
                $scope.showExcelTable=false;
            };

            $scope.checkData = function(){
                $scope.report=true;
                Dataset.checkData({},{'data': [data_projects, data_lists, data_strategies]}).$promise.then(function(data){
 
                    if ('empty' in data){
                        $scope.message = data['empty']
                        $scope.critical= "Empty"
                        $timeout(function(){
                          $scope.hasError.boolean= true;
                        });
                    }
                    else{
                        $scope.data_project_error = data['project'];
                        $scope.data_strategy_error = data['strategy'];
                        $scope.data_list_error = data['list'];
                        $scope.critical = data ['critical'];
                        $scope.message="";

                        if ($scope.critical == 0){
                            //$scope.message = "No Error";
                            $timeout(function(){
                              $scope.hasError.boolean= false;
                            });
                        };
                    }
                });
            };

            $scope.onGPLVersionSelected = function(){

                Dataset.getGPLnumber({},{'GPL': $scope.GPLVersionSelected.value.id}).$promise.then(function(data){
                    $scope.GPLNumberArray=data;
                    $scope.GPLNumberSelected = {value : ""};
                });
            };

            $scope.removeGPLNumberSelected = function(){
                $scope.GPLNumberSelected.value = "";
            };

            $scope.canSelect = function(){
                if ($scope.DBDatabaseSelected.value != ''){
                    if($scope.DBDatabaseSelected.value.name !='GPL'){
                        return true;
                    }
                    else{
                        if($scope.GPLNumberSelected.value != ''){
                            return true;
                        }
                        else{
                            return false;
                        }
                    }
                }
                else{
                    return false;
                }
            };

            $scope.addDatabase = function(){
                if($scope.DBDatabaseSelected.value.name != "GPL"){
                    $scope.database=$scope.DBDatabaseSelected.value.name;
                    $scope.success=$scope.DBDatabaseSelected.value.name + " has been selected";
                }
                else{
                     $scope.database = $scope.GPLNumberSelected.value.name;
                     $scope.success = $scope.GPLNumberSelected.value.name + " has been selected";
                }
            };

            function openDatabase(row,col){
                if(!$scope.dialog) {
                    $scope.dialog = ngDialog.open({
                        template: 'Database',
                        className: 'ngdialog-theme-flat ngdialog-theme-custom',
                        scope: $scope
                    });
                }

                $scope.dialog.closePromise.then(function(data) {

                    hot1.setDataAtCell(row, col, $scope.database);
                    $scope.DBDatabaseSelected.value = "";
                    $scope.GPLVersionSelected.value = "";
                    $scope.dialog = null;
                    $scope.warning="";
                    $scope.success="";
                    $scope.database=null;
                });
            };
            
            $scope.next = function() {
                $scope.uploadList=!$scope.uploadList;
                $scope.stepProgressBar_CheckData="active";
                Dataset.addFileNameToObjectFiles({},{'data_identifiant' : data_lists[0], 'data_available' : data_lists[7], 'data_filename':data_lists[8]}).$promise.then(function(data){
                    $scope.objectFiles=data['ObjectFiles'];
                });
            };

            $scope.previous = function(){ 
                $scope.uploadList=!$scope.uploadList;
                $scope.stepProgressBar_CheckData="";
            };

            // $scope.submit = function (){
            //     for(var i = 0; i < $scope.arrayFiles.length; i++){
            //         var resultInfo={'error':"",'critical':""};
            //         Upload.upload({
            //             url: '/upload/'+$scope.user.id+'/fileListUpload',
            //             fields: {'uid': $scope.user.id, 'dataset': 'tmp'},
            //             file: $scope.arrayFiles[i]
            //         }).progress(function (evt) {

            //         }).success(function (data, status, headers, config) {

            //         }).error(function (data, status, headers, config) {
            //         })
            //     }
            // };

            $scope.dropFiles = function(files){
                console.log(files);
            };

            $scope.addFiles = function(files){
                if(files == null){
                    return
                }
                for(var i = 0; i < files.length; i++){
                    addFileToObjectFiles(files[i])                
                }
            };

            function addFileToObjectFiles(object){
                if(object.name.split('.')[0] in $scope.objectFiles){
                    if($scope.objectFiles[object.name.split('.')[0]].name ==""){
                        $scope.objectFiles[object.name.split('.')[0]].name = object.name.split('.')[0];
                        $scope.objectFiles[object.name.split('.')[0]].file = object;
                        $scope.objectFiles[object.name.split('.')[0]].status='waiting';
                    }
                }
                else{
                    console.log( object.name.split('.')[0] +' file is not in your Filename List');
                }
            };

            $scope.remove = function(filename){
                if($scope.objectFiles[filename].filepath == ""){
                    $scope.objectFiles[filename].name="";// = {'name' : "", 'file': null}
                    $scope.objectFiles[filename].file=null;
                    $scope.objectFiles[filename].status="waiting";
                    $scope.objectFiles[filename].msg="";
                }
                else{
                    Dataset.removeFileListUpload({},{'filepath' : $scope.objectFiles[filename].filepath}).$promise.then(function(data){
                        $scope.canSubmit= {boolean : false};
                        if(data['boolean'] == true){
                            $scope.objectFiles[filename].name="";// = {'name' : "", 'file': null}
                            $scope.objectFiles[filename].file=null;
                            $scope.objectFiles[filename].status="waiting";
                            $scope.objectFiles[filename].filepath="";
                            $scope.objectFiles[filename].msg=data['msg'];
                        }
                        else{
                            $scope.objectFiles[filename].status="warning";
                            $scope.objectFiles[filename].msg=data['msg'];
                        }
                    });
                }
            };

            
            $scope.checkFile = function(){

                $scope.listKey= Object.keys($scope.objectFiles)
                for(var i = 0; i < $scope.listKey.length; i++){

                    if($scope.objectFiles[$scope.listKey[i]].name != "" && $scope.objectFiles[$scope.listKey[i]].filepath == ""){

                        var upload = Upload.upload({
                            url: '/upload/'+$scope.user.id+'/fileListUpload',
                            fields: {'uid': $scope.user.id, 'dataset': 'tmp'},
                            file : $scope.objectFiles[$scope.listKey[i]].file,
                            data : {'info':i}
                            
                        }).progress(function (evt) {

                        }).success(function (data, status, headers, config) {

                        }).error(function (data, status, headers, config) {

                        })

                        upload.then(function(data){
                            $scope.objectFiles[$scope.listKey[data['data']['number']]].status   = data['data']['status'];
                            $scope.objectFiles[$scope.listKey[data['data']['number']]].filepath = data['data']['filepath'];
                            $scope.objectFiles[$scope.listKey[data['data']['number']]].msg      = data['data']['msg'];
                            canSubmit();
                        });
                    }
                }
            };

            function canSubmit() {

                Dataset.canSubmit({},{"objectFiles" :  $scope.objectFiles}).$promise.then(function(data){
                    $scope.canSubmit.boolean = data['canSubmit'];
                });
            };


            $scope.submit = function() {
                //https://nakupanda.github.io/bootstrap3-dialog/

        //         $scope.dialog = new BootstrapDialog({
        //     message: function(dialogRef){
        //         var $message = $('<div>OK, this dialog has no header and footer, but you can close the dialog using this button: </div>');
        //         var $button = $('<button class="btn btn-primary btn-lg btn-block">Close the dialog</button>');
        //         $button.on('click', {dialogRef: dialogRef}, function(event){
        //             event.data.dialogRef.close();
        //         });
        //         $message.append($button);
        
        //         return $message;
        //     },
        //     closable: false
        // });
        // $scope.realize();
        // $scope.getModalHeader().hide();
        // $scope.getModalFooter().hide();
        // $scope.getModalBody().css('background-color', '#0088cc');
        // $scope.getModalBody().css('color', '#fff');
        // dialog.open();

                $scope.$textAndPic = $('<div></div>');
                $scope.$textAndPic.append('Please wait during the upload of your project<br />');
        
                $scope.dlg =   new BootstrapDialog({
                                title: 'Information',
                                message: $scope.$textAndPic,
                                buttons: [{
                                    label: 'close',
                                    action: function(dialogRef){
                                        dialogRef.close();
                                    }
                                }]
                            });
                $scope.dlg.realize();
                //$scope.dlg.getModalHeader().hide();
                $scope.dlg.getModalHeader().css('background-color', '#cccccc');
                $scope.dlg.open()

                // BootstrapDialog.show({
                //     title: 'Information',
                //     message: $textAndPic,
                //     buttons: [{
                //         label: 'close',
                //         action: function(dialogRef){
                //             dialogRef.close();
                //         }
                //     }]
                // });

                // var dlg = new BootstrapDialog({

                //     title: ' Notification',
                //     message: $('<div>!!!!Please wait during the upload of your project</div><div class="containesdots"><span class="dots"></span><span class="dots"></span><span class="dots"></span><span class="dots"></span><span class="dots"></span><span class="dots"></span><span class="dots"></span><span class="dots"></span><span class="dots"></span><span class="dots"></span></div>'),
                //     //message: $('');

                // })

                // dlg.open();
                Dataset.submit({},{'data_projects' : data_projects, 'data_strategies' : data_strategies, 'data_lists' : data_lists, "objectFiles" : $scope.objectFiles, "uid" : $scope.user.id }).$promise.then(function(data){
                    
                    $scope.dlg.close();

                    var color;
                    if (data['status'] == 'Danger'){
                        color= '#e6323d'
                    }
                    else{
                        color= '#3fac54'
                    }
                    

                    $scope.$textAndPic = $('<div></div>');
                    $scope.$textAndPic.append(data['message'] + '<br />');
                    $scope.$textAndPic.append('You are going to be relocated in 5 seconds');
                    $scope.dlg =   new BootstrapDialog({
                                title: data['status'],
                                message: $scope.$textAndPic,
                                buttons: [{
                                    label: 'close',
                                    action: function(dialogRef){
                                        dialogRef.close();
                                    }
                                }]
                            });
                    $scope.dlg.realize();
                    $scope.dlg.getModalHeader().css('background-color', color);
                    $scope.dlg.open()

                    $timeout(function(){ 
                          $scope.dlg.close();
                          $location.path('/user/'+$scope.user.id+'/myproject'); 
                          },5000);
                });
            };

            $scope.uid= "";
            $scope.filename="";
            $scope.download = function() {
                var toto = ['here we are']
                console.log($scope.user.id)
                $http({
                    method: 'POST',
                    contentType: "application/json",
                    url: '/createExcelForExport',
                    data : {'data_projects' : data_projects, 'data_strategies' : data_strategies, 'data_lists' : data_lists, 'uid' : $scope.user.id},
                }).success(function (data, status, headers){
                    $scope.uid= data['uid'];
                    $scope.filename=data['filename'];
                    window.open('/exportExcel'+'/'+data['uid']+'/'+data['tmp']+'/'+data['filename'] , '_self' , '')
                })
            };
            $(window).on('beforeunload',function(){alert('By now!')});
            window.onunload = function(e){
                
                 $http({
                            method: 'GET',
                            contentType: "application/json",
                            url: '/removeExcel'+'/'+$scope.uid+'/'+"tmp"+'/'+$scope.filename,
                            
                        }).success(function(data, status, event){
                            console.log(data)
                        }).the
                //e.returnValue = 'Coucou'

            }

            $scope.onExit = function(){
                console.log("heretoto1111")
            };
        });
    });
});

app.controller('userCtrl',
  function($scope, $rootScope, $routeParams, $log, $location, $window, User, Auth, Search, SearchHits) {

    $scope.is_logged = false;
    $rootScope.$on('loginCtrl.login', function (event, user) {
      $scope.user = user;
      $scope.is_logged = true;
    });

    $scope.action = 0; // show

    $scope.show_dataset = function(dataset){
      $location.url('/browse?dataset='+dataset.id);
    };


    $scope.dataset_new = function(){
      $location.url('/dataset');
    };

    $scope.convert_timestamp_to_date = function(UNIX_timestamp){
      if(UNIX_timestamp=='' || UNIX_timestamp===null || UNIX_timestamp===undefined) { return '';}
        var a = new Date(UNIX_timestamp*1000);
        var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
        var year = a.getFullYear();
        var month = months[a.getMonth()];
        var date = a.getDate();
        var hour = a.getHours();
        var min = a.getMinutes();
        var sec = a.getSeconds();
        var time = date + ',' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
        return time;
      };

    $scope.onSearch = function() {
      Search.search_index({'query': "status:public AND _all:"+$scope.search_sig+'*','from':0}).$promise.then(function(data){
        SearchHits.setHits(data);
        //$rootScope.search_result = data;
        $location.path('/search')
      });
    }

    $scope.email_hash = function(email) {
       var MD5=function(s){function L(k,d){return(k<<d)|(k>>>(32-d))}function K(G,k){var I,d,F,H,x;F=(G&2147483648);H=(k&2147483648);I=(G&1073741824);d=(k&1073741824);x=(G&1073741823)+(k&1073741823);if(I&d){return(x^2147483648^F^H)}if(I|d){if(x&1073741824){return(x^3221225472^F^H)}else{return(x^1073741824^F^H)}}else{return(x^F^H)}}function r(d,F,k){return(d&F)|((~d)&k)}function q(d,F,k){return(d&k)|(F&(~k))}function p(d,F,k){return(d^F^k)}function n(d,F,k){return(F^(d|(~k)))}function u(G,F,aa,Z,k,H,I){G=K(G,K(K(r(F,aa,Z),k),I));return K(L(G,H),F)}function f(G,F,aa,Z,k,H,I){G=K(G,K(K(q(F,aa,Z),k),I));return K(L(G,H),F)}function D(G,F,aa,Z,k,H,I){G=K(G,K(K(p(F,aa,Z),k),I));return K(L(G,H),F)}function t(G,F,aa,Z,k,H,I){G=K(G,K(K(n(F,aa,Z),k),I));return K(L(G,H),F)}function e(G){var Z;var F=G.length;var x=F+8;var k=(x-(x%64))/64;var I=(k+1)*16;var aa=Array(I-1);var d=0;var H=0;while(H<F){Z=(H-(H%4))/4;d=(H%4)*8;aa[Z]=(aa[Z]|(G.charCodeAt(H)<<d));H++}Z=(H-(H%4))/4;d=(H%4)*8;aa[Z]=aa[Z]|(128<<d);aa[I-2]=F<<3;aa[I-1]=F>>>29;return aa}function B(x){var k="",F="",G,d;for(d=0;d<=3;d++){G=(x>>>(d*8))&255;F="0"+G.toString(16);k=k+F.substr(F.length-2,2)}return k}function J(k){k=k.replace(/rn/g,"n");var d="";for(var F=0;F<k.length;F++){var x=k.charCodeAt(F);if(x<128){d+=String.fromCharCode(x)}else{if((x>127)&&(x<2048)){d+=String.fromCharCode((x>>6)|192);d+=String.fromCharCode((x&63)|128)}else{d+=String.fromCharCode((x>>12)|224);d+=String.fromCharCode(((x>>6)&63)|128);d+=String.fromCharCode((x&63)|128)}}}return d}var C=Array();var P,h,E,v,g,Y,X,W,V;var S=7,Q=12,N=17,M=22;var A=5,z=9,y=14,w=20;var o=4,m=11,l=16,j=23;var U=6,T=10,R=15,O=21;s=J(s);C=e(s);Y=1732584193;X=4023233417;W=2562383102;V=271733878;for(P=0;P<C.length;P+=16){h=Y;E=X;v=W;g=V;Y=u(Y,X,W,V,C[P+0],S,3614090360);V=u(V,Y,X,W,C[P+1],Q,3905402710);W=u(W,V,Y,X,C[P+2],N,606105819);X=u(X,W,V,Y,C[P+3],M,3250441966);Y=u(Y,X,W,V,C[P+4],S,4118548399);V=u(V,Y,X,W,C[P+5],Q,1200080426);W=u(W,V,Y,X,C[P+6],N,2821735955);X=u(X,W,V,Y,C[P+7],M,4249261313);Y=u(Y,X,W,V,C[P+8],S,1770035416);V=u(V,Y,X,W,C[P+9],Q,2336552879);W=u(W,V,Y,X,C[P+10],N,4294925233);X=u(X,W,V,Y,C[P+11],M,2304563134);Y=u(Y,X,W,V,C[P+12],S,1804603682);V=u(V,Y,X,W,C[P+13],Q,4254626195);W=u(W,V,Y,X,C[P+14],N,2792965006);X=u(X,W,V,Y,C[P+15],M,1236535329);Y=f(Y,X,W,V,C[P+1],A,4129170786);V=f(V,Y,X,W,C[P+6],z,3225465664);W=f(W,V,Y,X,C[P+11],y,643717713);X=f(X,W,V,Y,C[P+0],w,3921069994);Y=f(Y,X,W,V,C[P+5],A,3593408605);V=f(V,Y,X,W,C[P+10],z,38016083);W=f(W,V,Y,X,C[P+15],y,3634488961);X=f(X,W,V,Y,C[P+4],w,3889429448);Y=f(Y,X,W,V,C[P+9],A,568446438);V=f(V,Y,X,W,C[P+14],z,3275163606);W=f(W,V,Y,X,C[P+3],y,4107603335);X=f(X,W,V,Y,C[P+8],w,1163531501);Y=f(Y,X,W,V,C[P+13],A,2850285829);V=f(V,Y,X,W,C[P+2],z,4243563512);W=f(W,V,Y,X,C[P+7],y,1735328473);X=f(X,W,V,Y,C[P+12],w,2368359562);Y=D(Y,X,W,V,C[P+5],o,4294588738);V=D(V,Y,X,W,C[P+8],m,2272392833);W=D(W,V,Y,X,C[P+11],l,1839030562);X=D(X,W,V,Y,C[P+14],j,4259657740);Y=D(Y,X,W,V,C[P+1],o,2763975236);V=D(V,Y,X,W,C[P+4],m,1272893353);W=D(W,V,Y,X,C[P+7],l,4139469664);X=D(X,W,V,Y,C[P+10],j,3200236656);Y=D(Y,X,W,V,C[P+13],o,681279174);V=D(V,Y,X,W,C[P+0],m,3936430074);W=D(W,V,Y,X,C[P+3],l,3572445317);X=D(X,W,V,Y,C[P+6],j,76029189);Y=D(Y,X,W,V,C[P+9],o,3654602809);V=D(V,Y,X,W,C[P+12],m,3873151461);W=D(W,V,Y,X,C[P+15],l,530742520);X=D(X,W,V,Y,C[P+2],j,3299628645);Y=t(Y,X,W,V,C[P+0],U,4096336452);V=t(V,Y,X,W,C[P+7],T,1126891415);W=t(W,V,Y,X,C[P+14],R,2878612391);X=t(X,W,V,Y,C[P+5],O,4237533241);Y=t(Y,X,W,V,C[P+12],U,1700485571);V=t(V,Y,X,W,C[P+3],T,2399980690);W=t(W,V,Y,X,C[P+10],R,4293915773);X=t(X,W,V,Y,C[P+1],O,2240044497);Y=t(Y,X,W,V,C[P+8],U,1873313359);V=t(V,Y,X,W,C[P+15],T,4264355552);W=t(W,V,Y,X,C[P+6],R,2734768916);X=t(X,W,V,Y,C[P+13],O,1309151649);Y=t(Y,X,W,V,C[P+4],U,4149444226);V=t(V,Y,X,W,C[P+11],T,3174756917);W=t(W,V,Y,X,C[P+2],R,718787259);X=t(X,W,V,Y,C[P+9],O,3951481745);Y=K(Y,h);X=K(X,E);W=K(W,v);V=K(V,g)}var i=B(Y)+B(X)+B(W)+B(V);return i.toLowerCase()};
       return MD5(email);
    };
    /*
    User.is_authenticated().$promise.then(function(data) {
        if(data.user !== null) {
         $scope.user = data.user;
         $scope.user['is_admin'] = data.is_admin;
         $scope.is_logged = true;
         Auth.setUser($scope.user);
       }
    });
    */

    $scope.logout = function() {
        $scope.user = null;
        $scope.is_logged = false;
        Auth.setUser(null);
        delete $window.sessionStorage.token;
        $location.path('/');
    };

});

app.controller('browseCtrl',
  function($scope, $rootScope, $routeParams, $log,$cookies, $cookieStore, $location, $window, Dataset, User, Upload, Auth, ngDialog) {
      //$scope.list = [{'title': 'test1', 'items': [{'title': 'subtest1'},{'title': 'subtest2'}]}];
      $scope.user = Auth.getUser();

      if($window.sessionStorage.token) {
          $scope.token = $window.sessionStorage.token;
      }

      $scope.collaborator = null;
      $scope.location = location.host;
      $scope.urlabs = $location.absUrl();
      var nodes = new vis.DataSet();
      var edges = new vis.DataSet();
      var network;

      var options = {
        layout: {
          randomSeed: undefined,
          improvedLayout:true,
          hierarchical: {
            enabled:true,
            levelSeparation: 150,
            nodeSpacing: 100,
            treeSpacing: 200,
            blockShifting: true,
            edgeMinimization: true,
            parentCentralization: true,
            direction: 'UD',        // UD, DU, LR, RL
            sortMethod: 'hubsize'   // hubsize, directed
          }
        }
      };
      $scope.factors = [];
      $scope.assay={}

      var container = document.getElementById('mynetwork');
      


      var params = $location.search();
      ////console.log(params);
      console.log(params);
      if(params['dataset'] !== undefined) {
        $scope.collection = "";
        if (params['dataset'].includes("GST")){
          $scope.collection = 'studies';
        };
        if (params['dataset'].includes("GPR")){
          $scope.collection = 'projects';
        };
        if (params['dataset'].includes("GSR")){
          $scope.collection = 'strategies';
        };
        if (params['dataset'].includes("GUL")){
          $scope.collection = 'lists';
        };

        Dataset.get({'filter':params['dataset'],'from':'None','to':'None','collection':$scope.collection,'field':'id'}).$promise.then(function(data){
          $scope.data = data.request;
          console.log($scope.data);

          
          if($scope.data.status != 'public' && ($scope.user == undefined || $scope.user.id != $scope.data.owner )){
            console.log($scope.data.status);
            console.log($scope.data.owner);
            console.log($scope.user);
            $scope.data = {};
            $scope.data['id'] = 'ERROR';
            $scope.data['title'] = 'You are not authorized to access this resource'
            return $scope.data
          }
          Dataset.get({'filter':$scope.data.owner,'from':'None','to':'None','collection':'users','field':'id'}).$promise.then(function(result){
              $scope.owner = result.request;
          });
         
          if($scope.collection == 'studies'){
            console.log($scope.data)
            document.getElementById('mynetwork').style.display = "none";
            //Get info on project/studies and owner
            Dataset.get({'filter':$scope.data.projects,'from':'None','to':'None','collection':'projects','field':'id'}).$promise.then(function(result){
              $scope.info_project = result.request.title;
            });
            

            $scope.data.strategies = $scope.data.strategies_id.split(',');
            $scope.data.lists = $scope.data.lists_id.split(',');
            if($scope.data.warnings != undefined){
              $scope.data.warnings = $scope.data.warnings.split(',');
            }
            if($scope.data.info != undefined){
              $scope.data.info = $scope.data.info.split(',');
            }
            if($scope.data.critical != undefined){
              $scope.data.critical = $scope.data.critical.split(',');
            }

          };

          if($scope.collection == 'strategies'){
            console.log("TRUE");
            document.getElementById('mynetwork').style.display = "none";
            console.log($scope.data);

            Dataset.get({'filter':$scope.data.projects,'from':'None','to':'None','collection':'projects','field':'id'}).$promise.then(function(result){
              $scope.info_project = result.request.title;
              console.log("here");
              console.log(result.request);
            });
            
            Dataset.get({'filter':$scope.data.studies,'from':'None','to':'None','collection':'studies','field':'id'}).$promise.then(function(result){
              $scope.info_study = result.request.title;
              console.log("here");
              console.log(result.request.title);
            });

            $scope.data.lists = $scope.data.lists_id.split(',');

            if($scope.data.warnings != undefined){
              $scope.data.warnings = $scope.data.warnings.split(',');
            }
            if($scope.data.info != undefined){
              $scope.data.info = $scope.data.info.split(',');
            }
            if($scope.data.critical != undefined){
              $scope.data.critical = $scope.data.critical.split(',');
            }
            
            // $scope.data.factors = $scope.data.factors.split(',');
            // for(var i=0;i < $scope.data.factors.length; i++){
            //   console.log($scope.data.factors[i]);
            //   var id_factor = $scope.data.factors[i];
            //   Dataset.get({'filter':id_factor,'from':'None','to':'None','collection':'factors','field':'id'}).$promise.then(function(data){
            //     $scope.factors.push(data.request);
            //   });

            // }
          };

          if($scope.collection == 'lists'){
            console.log($scope.data);

            Dataset.get({'filter':$scope.data.projects,'from':'None','to':'None','collection':'projects','field':'id'}).$promise.then(function(result){
              $scope.info_project = result.request.title;
            });
            
            Dataset.get({'filter':$scope.data.studies,'from':'None','to':'None','collection':'studies','field':'id'}).$promise.then(function(result){
              $scope.info_study = result.request.title;
            });

            if($scope.data.warnings != undefined){
              $scope.data.warnings = $scope.data.warnings.split(',');
            }
            if($scope.data.info != undefined){
              $scope.data.info = $scope.data.info.split(',');
            }
            if($scope.data.critical != undefined){
              $scope.data.critical = $scope.data.critical.split(',');
            }

            document.getElementById('mynetwork').style.display = "none";
            $scope.data.studies = $scope.data.studies.split(',');
            $scope.data.strategies = $scope.data.strategies.split(',');
            for(var z=0;z<$scope.data.strategies.length;z++){
              Dataset.get({'filter':$scope.data.strategies[z],'from':'None','to':'None','collection':'strategies','field':'id'}).$promise.then(function(data){
                $scope.strategies = data.request;
                $scope.strategies.factors = $scope.strategies.factors.split(',');
                for(var i=0;i < $scope.assays.factors.length; i++){
                  console.log($scope.assays.factors[i]);
                  var id_factor = $scope.assays.factors[i];
                  Dataset.get({'filter':id_factor,'from':'None','to':'None','collection':'factors','field':'id'}).$promise.then(function(data){
                    $scope.factors.push(data.request);
                  });

                }
              });
            }
          };

          //Network project
          if($scope.collection == 'projects'){
            //Init edge/node variable
            console.log($scope.data.studies_id);
            $scope.data_id=$scope.data.project_id
            if ($scope.data.pubmed == ""){
                $scope.data.pubmed = "-";
            }
       
            else{
                $scope.data.pubmed = $scope.data.pubmed.split(',');
            }

            if ($scope.data.contributors == ""){
                $scope.data.contributor= "-";
            }
            else{
                $scope.data.contributor = $scope.data.contributors.split(',');
            }

            
            if($scope.data.warnings != undefined){
              $scope.data.warnings = $scope.data.warnings.split(',');
            }
            if($scope.data.info != undefined){
              $scope.data.info = $scope.data.info.split(',');
            }
            if($scope.data.critical != undefined){
              $scope.data.critical = $scope.data.critical.split(',');
            }
            // return
            // var nodeId = 1
            // var nodeObj = {};
            // var nodeProject = [];
            // var edgeProject = [];
            // var selectedNode;
            // var selecteddata;

            // data.request.studies = data.request.studies.split(',')
            // data.request.lists =  data.request.lists.split(',')
            // data.request.strategies =  data.request.strategies.split(',')
            // //init root as project
            // nodeObj[data.request.id] = nodeId;
            // nodeProject.push({'id':nodeId,'label':data.request.id,'shape':'box','level':1})

            // //Create node + node index
            // for(var index in data.request.studies){
            //   nodeId ++;
            //   var obj = data.request.studies[index];
            //   nodeObj[obj] = nodeId;
            //   nodeProject.push({'id':nodeId,'label':obj,'shape':'circle','color':'#93c54b','level':2})
            // }
            // for(var index in data.request.lists){
            //   nodeId ++;
            //   var obj = data.request.lists[index];
            //   nodeObj[obj] = nodeId;
            //   nodeProject.push({'id':nodeId,'label':obj,'shape':'database','color':'#d9534f','level':4})
            // }
            // for(var index in data.request.strategies){
            //   nodeId ++;
            //   var obj = data.request.strategies[index];
            //   nodeObj[obj] = nodeId;
            //   nodeProject.push({'id':nodeId,'label':obj,'shape':'triangle','color':'grey','level':3})
            // }

            // //Create edges from root
            // for(var index in data.request.studies){
            //   var obj = data.request.studies[index];
            //   var from = 1;
            //   var to = nodeObj[obj];
            //   edgeProject.push({'from':from,'to':to})
            // }

            // //create all remining edges
            // for(var index in data.request.edges){
            //   var from = nodeObj[index];
            //   for(var asso in data.request.edges[index]){
            //     var to = nodeObj[data.request.edges[index][asso]];
            //     edgeProject.push({'from':from,'to':to})
            //   }
            //   //var from = 1;
            //   //var to = nodeObj[obj];
            //   //edgeProject.push({'from':from,'to':to})
            // }


            // // create an array with nodes
            // nodes.add(nodeProject);

            // // create an array with edges
            // edges.add(edgeProject);

            // // create a network

            // // provide the data in the vis format
            // var datanet = {
            //     nodes: nodes,
            //     edges: edges
            // };
            
            // network = new vis.Network(container, datanet, options);
            

            // // initialize your network!
            
            // network.on( 'click', function(properties) {
            //     var ids = properties.nodes;
            //     var clickedNodes = nodes.get(ids);
            //     selectedNode = clickedNodes[0]['label'];
            //     document.getElementById('information').innerHTML = selectedNode;
            //     document.getElementById('viewinfo').style.display = "inline";
            // });
          } //End network project
        });
      }
      $scope.showInfo = function(){
        var dataset = document.getElementById('information').innerHTML;
        $location.url('/browse?dataset='+dataset);
      }
      $scope.display = function(id){
        $location.url('/browse?dataset='+id);
      }


      $scope.getProject = function (id){
        Dataset.download({'uid':$scope.user.id,'id':id}).$promise.then(function(data){
          if(data['msg']){
            $scope.msg = data['msg'];
            return false
          }
          //var link = document.createElement("a");
          //console.log(data['url'])
          //link.href = data['url'];
          //link.click();
        });
      };

      $scope.addToWorkspace = function(id){
        if ($scope.user != null && $scope.user != undefined ){
            var selectedID = $scope.user.selectedID
            if (selectedID.split(',').indexOf(id) == -1){
              if (selectedID == "" || selectedID == undefined){
                selectedID = id;
                $scope.user.selectedID = selectedID;
              }
              else {
                selectedID = selectedID+','+id;
                $scope.user.selectedID = selectedID;
              }
      
            }
            
            $scope.user.$save({'uid': $scope.user.id}).then(function(data){
                    $scope.user = data;
                    console.log(data);
            });
        }
        else {
          $cookieStore.put('selectedID', id);
        }
      }

      $scope.file_upload = function(file,type) {
            console.log(file);
            Upload.upload({
                url: '/upload/'+$scope.user.id+'/'+$scope.data.id+'/file_upload',
                fields: {'uid': $scope.user.id, 'dataset': $scope.data.projects,'type':type, 'name':file.name, 'sid':$scope.data.id},
                file: file
            }).progress(function (evt) {
                var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
                console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
            }).success(function (data, status, headers, config) {
                console.log('file ' + config.file.name + ' uploaded.');
                alert(data.msg);


            }).error(function (data, status, headers, config) {
                console.log('error status: ' + status);
                alert(data.msg)
            })
            
      };

      $scope.signature_upload = function(excel_file,pid) {
            ////console.log(signature_file);
            var resultInfo={'error':"",'critical':""};
            Upload.upload({
                url: '/upload/'+$scope.user.id+'/excelupload',
                fields: {'uid': $scope.user.id, 'dataset': 'tmp'},
                file: excel_file
            }).progress(function (evt) {
                var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
                //document.getElementById("bgimg").style.display = "block";
                console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
                ngDialog.open({ template: 'checking', className: 'ngdialog-theme-default'})
            }).success(function (data, status, headers, config) {
                if (data.status == "0"){
                  console.log('file ' + config.file.name + ' uploaded.');
                  console.log(data.error_assay);
                  resultInfo['error_p'] = data.error_project;
                  resultInfo['error_s'] = data.error_study;
                  resultInfo['error_a'] = data.error_assay;
                  resultInfo['error_f'] = data.error_factor;
                  resultInfo['error_sig'] = data.error_signature;
                  resultInfo['critical'] = data.critical;
                  resultInfo['file'] = data.file;
                  resultInfo['pid'] = pid;
                  ngDialog.close();
                  ngDialog.open({ template: 'firstDialogId', scope: $scope, className: 'ngdialog-theme-default',data: resultInfo})
                }
                if (data.status == '1'){
                  alert(data.msg);
                }
                //document.getElementById("bgimg").style.display = "none";
            }).error(function (data, status, headers, config) {
                ////console.log('error status: ' + status);
            })
            console.log(resultInfo);
            
      };
      $scope.upExcel = function (obj,pid){
        console.log(obj);
        ngDialog.open({ template: 'saving', className: 'ngdialog-theme-default'})
        User.update({'uid': $scope.user.id, 'file': obj, 'pid' : pid}).$promise.then(function(data){
                alert(data.msg);
                ngDialog.close();
        });
      }

      $scope.convert_timestamp_to_date = function(UNIX_timestamp){
          if(UNIX_timestamp=='' || UNIX_timestamp===null || UNIX_timestamp===undefined) { return '';}
          var a = new Date(UNIX_timestamp*1000);
          var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
          var year = a.getFullYear();
          var month = months[a.getMonth()];
          var date = a.getDate();
          var hour = a.getHours();
          var min = a.getMinutes();
          var sec = a.getSeconds();
          var time = date + ',' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
          return time;
        }

      $scope.switch = function(project){
        var r = confirm("You are about to make your project public.");
        if (r == true) {
            Dataset.pending({'project':project}).$promise.then(function(data){
              alert(data.msg);
            });
        }
      }

      

      $scope.can_edit = function() {
          if ($scope.user === null){
            return false;
          };
          if($scope.dataset !== undefined && $scope.user !== undefined) {
            if($scope.dataset.status != "private") {
                return false;
            }
            if($scope.dataset.owner == $scope.user.id) {
                return true;
            }
            if($scope.dataset.collaborators.indexOf($scope.user.id)>=0) {
                return true;
            }
            if($scope.user['admin'] !== undefined && $scope.user['admin']) {
                return true;
            }
          }
          else {
              return false;
          }
      }
});

app.controller('databaseCtrl',
  function($scope, $rootScope, $routeParams, $log, $location, $window, User, Dataset, Auth, ngDialog, $filter, ngTableParams) {
      //$scope.list = [{'title': 'test1', 'items': [{'title': 'subtest1'},{'title': 'subtest2'}]}];
      $scope.user = Auth.getUser();
      if($window.sessionStorage.token) {
          $scope.token = $window.sessionStorage.token;
      }
      $scope.collaborator = null;
      $scope.location = location.host;
      $scope.pfrom = 0;
      $scope.pto = 25;
      $scope.sfrom = 0;
      $scope.sto = 25;
      $scope.afrom = 0;
      $scope.ato = 25;
      $scope.sgfrom = 0;
      $scope.sgto = 25;

      Dataset.get({'filter':'private','from':$scope.pfrom,'to': $scope.pto,'collection':'projects','field':'status','all_info':'true'}).$promise.then(function(data){
        $scope.projects = data.request;
        //console.log('start');
        //
        //console.log($scope.projects[0].lists_id);
        //console.log('stop');
        $scope.projects_number = data.project_number;
        $scope.studies_number = data.study_number;
        $scope.strategies_number = data.strategy_number;
        $scope.lists_number = data.list_number;
      });



      $scope.showStudies = function(){
        Dataset.get({'filter':'private','from':$scope.sfrom,'to': $scope.sto,'collection':'studies','field':'status'}).$promise.then(function(data){
            $scope.studies = data.request;
            
          });
      };

      $scope.showStrategies = function(){
        Dataset.get({'filter':'private','from':$scope.afrom,'to': $scope.ato,'collection':'strategies','field':'status'}).$promise.then(function(data){
            $scope.strategies = data.request;
          });
      };

      $scope.showLists = function(){
        Dataset.get({'filter':'private','from':$scope.sgfrom,'to': $scope.sgto,'collection':'lists','field':'status'}).$promise.then(function(data){
            $scope.lists = data.request;
            console.log($scope.lists);
          });
      };

      $scope.more = function(type){

        if(type=="projects"){
          console.log($scope.pfrom)
          console.log($scope.pto)
          $scope.pfrom = $scope.pto + 0;
          $scope.pto = $scope.pto + 25;
          console.log($scope.pfrom)
          console.log($scope.pto)
          Dataset.get({'filter':'private','from':$scope.pfrom,'to': $scope.pto,'collection':'projects','field':'status'}).$promise.then(function(data){
            $scope.projects = data.request;
          });
        }
        else if(type=="studies"){
          $scope.sfrom = $scope.sto + 0;
          $scope.sto = $scope.sto + 25;
          Dataset.get({'filter':'private','from':$scope.sfrom,'to': $scope.sto,'collection':'studies','field':'status'}).$promise.then(function(data){
            $scope.studies = data.request;
          });
        }
        else if(type=="strategies"){
          $scope.afrom = $scope.ato + 0;
          $scope.ato = $scope.ato + 25;
          Dataset.get({'filter':'privateate','from':$scope.afrom,'to': $scope.ato,'collection':'strategies','field':'status'}).$promise.then(function(data){
            $scope.strategies = data.request;
          });
        }
        else if(type=="lists"){
        console.log("here")
          $scope.sgfrom = $scope.sgto + 0;
          $scope.sgto = $scope.sgto + 25;
          Dataset.get({'filter':'private','from':$scope.sgfrom,'to': $scope.sgto,'collection':'lists','field':'status'}).$promise.then(function(data){
            $scope.lists = data.request;
            console.log(data);
          });
        }
        else{
            $scope.msg="Error - Please contact the administrator";
        }
      };

      $scope.back = function(type){

        if(type=="projects"){
          $scope.pfrom = $scope.pfrom - 25 ;
          $scope.pto = $scope.pto - 25;
          Dataset.get({'filter':'private','from':$scope.pfrom,'to': $scope.pto,'collection':'projects','field':'status'}).$promise.then(function(data){
            $scope.projects = data.request;
          });
        }
        else if(type=="studies"){
          $scope.sfrom = $scope.sfrom - 25 ;
          $scope.sto = $scope.sto - 25;
          Dataset.get({'filter':'private','from':$scope.sfrom,'to': $scope.sto,'collection':'studies','field':'status'}).$promise.then(function(data){
            $scope.studies = data.request;
          });
        }
        else if(type=="strategies"){
          $scope.afrom = $scope.afrom - 25;
          $scope.ato = $scope.ato - 25;
          Dataset.get({'filter':'private','from':$scope.afrom,'to': $scope.ato,'collection':'strategies','field':'status'}).$promise.then(function(data){
            $scope.studies = data.request;
          });
        }
        else if(type=="lists"){
          $scope.sgfrom = $scope.sgfrom - 25;
          $scope.sgto = $scope.sgto - 25;
          Dataset.get({'filter':'private','from':$scope.sgfrom,'to': $scope.sgto,'collection':'lists','field':'status'}).$promise.then(function(data){
            $scope.lists = data.request;
          });
        }
        else{
            $scope.msg="Error - Please cotnact the administrator";
        }

      };


      $scope.convert_timestamp_to_date = function(UNIX_timestamp){
          if(UNIX_timestamp=='' || UNIX_timestamp===null || UNIX_timestamp===undefined) { return '';}
          var a = new Date(UNIX_timestamp*1000);
          var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
          var year = a.getFullYear();
          var month = months[a.getMonth()];
          var date = a.getDate();
          var hour = a.getHours();
          var min = a.getMinutes();
          var sec = a.getSeconds();
          var time = date + ',' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
          return time;
        };

      $scope.open_info = function(id){
        ngDialog.open({ template: id, className: 'ngdialog-theme-default'});
      };    

});

app.controller('ontologiesCtrl',
    function ($scope,$rootScope, $log, Auth, User, Dataset, $location) {
      $scope.msg = "Dashboard Tools";
      $scope.selected_organism = 'none';
      console.log($scope.selected_organism);

      $scope.get_onto = function(val,database) {
        ////console.log(database);
        return Dataset.ontologies({},{'database':database,'search':
          val}).$promise.then(function(data){
            return data.map(function(item){
                 return item;
           });
         });
       };

      $scope.selected_tissue = function(item, model,label){
         $scope.selected_tissue = item;
         document.getElementById('selected_tissue').style.display = "block";

      };

      $scope.selected_organism = function(item, model,label){
         $scope.selected_organism = item;
         document.getElementById('organism_results').style.display = "block";
      };

      $scope.selected_pathologies = function(item, model,label){
         $scope.selected_pathologies = item;
         document.getElementById('selected_pathologies').style.display = "block";
      };

      $scope.selected_molecule = function(item, model,label){
         $scope.selected_molecule = item;
         document.getElementById('selected_molecule').style.display = "block";
      };

      $scope.selected_technology= function(item, model,label){
         $scope.selected_technology = item;
         document.getElementById('selected_technology').style.display = "block";
      };

});

app.controller('adminCtrl',
  function ($scope, $rootScope, $routeParams, $log, $location, $filter, $window, User, Auth, Admin, Dataset, ngTableParams) {
      $scope.msg = null;
      var user = Auth.getUser();
      if (user === null || user === undefined || ! user.admin) {
          $location.path('');
      }
      $scope.project_number = 0;
      $scope.study_number = 0;
      $scope.assay_number = 0;
      $scope.signature_number = 0;
      $scope.users = null;
      $scope.pendings = null;
      Admin.dbinfo().$promise.then(function(data){
        $scope.project_number = data['project_number'];
        $scope.study_number = data['study_number'];
        $scope.strategy_number = data['strategy_number'];
        $scope.list_number = data['list_number'];
        $scope.users = data.users;
        $scope.pendings = data.pendings;
      });

      $scope.validate = function(project) {
        Admin.validate({'project':project}).$promise.then(function(data){
          $scope.msg=data.msg;
        });
      }

      $scope.Rdata = function(project) {
        Admin.validate({'project':""}).$promise.then(function(data){
          $scope.msg=data.msg;
        });
      }

       $scope.annofile = function(project) {
        Admin.validate({'project':"gohomo"}).$promise.then(function(data){
          $scope.msg=data.msg;
        });
      }

      $scope.unvalidation = function(project) {
        Admin.unvalidate({'project':project}).$promise.then(function(data){
          $scope.msg=data.msg;
        });
      }

});




app.service('Auth', function() {
    var user =null;
    return {
        getUser: function() {
            return user;
        },
        setUser: function(newUser) {
            user = newUser;
        },
        isConnected: function() {
            return !!user;
        }
    };
});

app.service('SearchHits', function() {
    var hits =null;
    return {
        getHits: function() {
            return hits;
        },
        setHits: function(results) {
            hits = results;
        }
    };
});
