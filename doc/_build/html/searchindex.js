Search.setIndex({envversion:46,filenames:["index","modules","prisoner","prisoner.gateway","prisoner.gateway.tests","prisoner.persistence","prisoner.server","prisoner.tests","prisoner.workflow","prisoner.workflow.tests","tutorials","tutorials.demo","tutorials.gettingstarted","tutorials.helloworld","tutorials.keyconcepts"],objects:{"":{prisoner:[2,0,0,"-"]},"prisoner.SocialObjects":{Address:[2,1,1,""],Collection:[2,1,1,""],Comment:[2,1,1,""],DateTimeJSONHandler:[2,1,1,""],Event:[2,1,1,""],Image:[2,1,1,""],InvalidTransformationLevelError:[2,4,1,""],Note:[2,1,1,""],Person:[2,1,1,""],Place:[2,1,1,""],SocialObject:[2,1,1,""]},"prisoner.SocialObjects.Address":{country:[2,3,1,""],formatted:[2,3,1,""],locality:[2,3,1,""],postalCode:[2,3,1,""],region:[2,3,1,""],streetAddress:[2,3,1,""]},"prisoner.SocialObjects.Collection":{objects:[2,3,1,""]},"prisoner.SocialObjects.Comment":{inReplyTo:[2,3,1,""]},"prisoner.SocialObjects.DateTimeJSONHandler":{flatten:[2,2,1,""],restore:[2,2,1,""]},"prisoner.SocialObjects.Event":{attending:[2,3,1,""],endTime:[2,3,1,""],maybeAttending:[2,3,1,""],notAttending:[2,3,1,""],startTime:[2,3,1,""]},"prisoner.SocialObjects.Image":{fullImage:[2,3,1,""]},"prisoner.SocialObjects.Person":{image:[2,3,1,""]},"prisoner.SocialObjects.Place":{address:[2,3,1,""],position:[2,3,1,""],position_as_dict:[2,2,1,""]},"prisoner.SocialObjects.SocialObject":{author:[2,3,1,""],base_transform_name:[2,2,1,""],content:[2,3,1,""],displayName:[2,3,1,""],get_friendly_name:[2,2,1,""],id:[2,3,1,""],location:[2,3,1,""],provider:[2,3,1,""],published:[2,3,1,""],tags:[2,3,1,""],transform_hash:[2,2,1,""],transform_reduce:[2,2,1,""],updated:[2,3,1,""],url:[2,3,1,""]},"prisoner.gateway":{FacebookGateway:[3,0,0,"-"],LastfmGateway:[3,0,0,"-"],ServiceGateway:[3,0,0,"-"],TwitterGateway:[3,0,0,"-"],tests:[4,0,0,"-"]},"prisoner.gateway.FacebookGateway":{Album:[3,1,1,""],Albums:[3,1,1,""],Book:[3,1,1,""],Checkin:[3,1,1,""],Checkins:[3,1,1,""],Comment:[3,1,1,""],Comments:[3,1,1,""],FacebookServiceGateway:[3,1,1,""],Friends:[3,1,1,""],Like:[3,1,1,""],Likes:[3,1,1,""],Movie:[3,1,1,""],Music:[3,1,1,""],Page:[3,1,1,""],Photo:[3,1,1,""],Photos:[3,1,1,""],Status:[3,1,1,""],StatusList:[3,1,1,""],Tags:[3,1,1,""],User:[3,1,1,""],check_none:[3,5,1,""]},"prisoner.gateway.FacebookGateway.Album":{albumType:[3,3,1,""],comments:[3,3,1,""],count:[3,3,1,""],coverPhoto:[3,3,1,""],likes:[3,3,1,""],photos:[3,3,1,""],privacy:[3,3,1,""]},"prisoner.gateway.FacebookGateway.Checkin":{checkinType:[3,3,1,""],image:[3,3,1,""]},"prisoner.gateway.FacebookGateway.FacebookServiceGateway":{Album:[3,2,1,""],Book:[3,2,1,""],Checkin:[3,2,1,""],Friends:[3,2,1,""],Like:[3,2,1,""],Movie:[3,2,1,""],Music:[3,2,1,""],Photo:[3,2,1,""],Session:[3,2,1,""],Status:[3,2,1,""],User:[3,2,1,""],complete_authentication:[3,2,1,""],generate_permissions_list:[3,2,1,""],get_comments:[3,2,1,""],get_graph_data:[3,2,1,""],get_likes:[3,2,1,""],get_value:[3,2,1,""],parse_comments:[3,2,1,""],parse_json:[3,2,1,""],parse_likes:[3,2,1,""],parse_location:[3,2,1,""],parse_tags:[3,2,1,""],post_graph_data:[3,2,1,""],request_authentication:[3,2,1,""],request_handler:[3,2,1,""],restore_authentication:[3,2,1,""],str_to_time:[3,2,1,""]},"prisoner.gateway.FacebookGateway.Page":{category:[3,3,1,""],image:[3,3,1,""]},"prisoner.gateway.FacebookGateway.Photo":{comments:[3,3,1,""],height:[3,3,1,""],image:[3,3,1,""],likes:[3,3,1,""],position:[3,3,1,""],tags:[3,3,1,""],thumbnail:[3,3,1,""],width:[3,3,1,""]},"prisoner.gateway.FacebookGateway.Status":{comments:[3,3,1,""],likes:[3,3,1,""],link:[3,3,1,""],privacy:[3,3,1,""]},"prisoner.gateway.FacebookGateway.User":{bio:[3,3,1,""],birthday:[3,3,1,""],education:[3,3,1,""],email:[3,3,1,""],firstName:[3,3,1,""],gender:[3,3,1,""],hometown:[3,3,1,""],interestedIn:[3,3,1,""],languages:[3,3,1,""],lastName:[3,3,1,""],location:[3,3,1,""],middleName:[3,3,1,""],politicalViews:[3,3,1,""],relationshipStatus:[3,3,1,""],religion:[3,3,1,""],significantOther:[3,3,1,""],timezone:[3,3,1,""],updatedTime:[3,3,1,""],username:[3,3,1,""],work:[3,3,1,""]},"prisoner.gateway.LastfmGateway":{LastfmServiceGateway:[3,1,1,""],Playlist:[3,1,1,""],Track:[3,1,1,""]},"prisoner.gateway.LastfmGateway.LastfmServiceGateway":{Comment:[3,2,1,""],Image:[3,2,1,""],Playlist:[3,2,1,""],Session:[3,2,1,""],Track:[3,2,1,""],complete_authentication:[3,2,1,""],request_authentication:[3,2,1,""],restore_authentication:[3,2,1,""]},"prisoner.gateway.LastfmGateway.Track":{artist:[3,3,1,""],get_friendly_name:[3,2,1,""],tag:[3,3,1,""],title:[3,3,1,""],transform_artist:[3,2,1,""]},"prisoner.gateway.ServiceGateway":{SARHeaders:[3,1,1,""],ServiceGateway:[3,1,1,""],SocialActivityResponse:[3,1,1,""],WrappedResponse:[3,1,1,""]},"prisoner.gateway.ServiceGateway.SARHeaders":{object_type:[3,3,1,""],operation:[3,3,1,""],payload:[3,3,1,""],provider:[3,3,1,""],wrapped_headers:[3,3,1,""]},"prisoner.gateway.ServiceGateway.ServiceGateway":{Image:[3,2,1,""],Session:[3,2,1,""],complete_authentication:[3,2,1,""],request_authentication:[3,2,1,""],request_handler:[3,2,1,""],restore_authentication:[3,2,1,""]},"prisoner.gateway.ServiceGateway.SocialActivityResponse":{content:[3,3,1,""],headers:[3,3,1,""]},"prisoner.gateway.ServiceGateway.WrappedResponse":{headers:[3,3,1,""],social_object:[3,3,1,""]},"prisoner.gateway.TwitterGateway":{Timeline:[3,1,1,""],TwitterServiceGateway:[3,1,1,""]},"prisoner.gateway.TwitterGateway.Timeline":{id:[3,3,1,""]},"prisoner.gateway.TwitterGateway.TwitterServiceGateway":{Session:[3,2,1,""],Timeline:[3,2,1,""],complete_authentication:[3,2,1,""],request_authentication:[3,2,1,""]},"prisoner.gateway.tests":{FacebookGatewayTests:[4,0,0,"-"],LastfmGatewayTests:[4,0,0,"-"]},"prisoner.gateway.tests.FacebookGatewayTests":{BaseFacebookGatewayTestCase:[4,1,1,""],GetPermissionsForPolicyTestCase:[4,1,1,""],InitialiseTestCase:[4,1,1,""],StatusTestCase:[4,1,1,""],UserTestCase:[4,1,1,""]},"prisoner.gateway.tests.FacebookGatewayTests.BaseFacebookGatewayTestCase":{create_user_all_permissions:[4,2,1,""],create_user_no_permissions:[4,2,1,""],get_bad_processor:[4,2,1,""],get_empty_processor:[4,2,1,""],get_good_processor:[4,2,1,""],get_good_props:[4,2,1,""],post_graph_data:[4,2,1,""],setUp:[4,2,1,""],set_test_user_attributes:[4,2,1,""]},"prisoner.gateway.tests.FacebookGatewayTests.GetPermissionsForPolicyTestCase":{test_bad_policy:[4,2,1,""],test_good_policy:[4,2,1,""]},"prisoner.gateway.tests.FacebookGatewayTests.InitialiseTestCase":{test_bad_policy:[4,2,1,""],test_bad_props:[4,2,1,""],test_bad_token:[4,2,1,""],test_good_policy:[4,2,1,""],test_good_props:[4,2,1,""],test_good_token:[4,2,1,""],test_no_policy:[4,2,1,""],test_no_props:[4,2,1,""],test_no_token:[4,2,1,""]},"prisoner.gateway.tests.FacebookGatewayTests.StatusTestCase":{test_post:[4,2,1,""]},"prisoner.gateway.tests.FacebookGatewayTests.UserTestCase":{test_good_get:[4,2,1,""],test_post:[4,2,1,""]},"prisoner.gateway.tests.LastfmGatewayTests":{BaseLastfmServiceGatewayTestCase:[4,1,1,""],ImageTestCase:[4,1,1,""]},"prisoner.gateway.tests.LastfmGatewayTests.BaseLastfmServiceGatewayTestCase":{setUp:[4,2,1,""]},"prisoner.gateway.tests.LastfmGatewayTests.ImageTestCase":{test_get_failure:[4,2,1,""],test_get_success:[4,2,1,""]},"prisoner.persistence":{PersistenceManager:[5,0,0,"-"]},"prisoner.persistence.PersistenceManager":{PersistenceManager:[5,1,1,""]},"prisoner.persistence.PersistenceManager.PersistenceManager":{close_connection:[5,2,1,""],do_build_schema:[5,2,1,""],experimental_design:[5,3,1,""],get_existing_provider_auth:[5,2,1,""],get_participant:[5,2,1,""],get_props:[5,2,1,""],get_table:[5,2,1,""],post_response:[5,2,1,""],post_response_json:[5,2,1,""],props:[5,3,1,""],rebuild_engine:[5,2,1,""],register_participant:[5,2,1,""],register_participant_with_provider:[5,2,1,""],validate_design:[5,2,1,""]},"prisoner.server":{webservice:[6,0,0,"-"]},"prisoner.server.webservice":{PRISONER:[6,1,1,""],create_app:[6,5,1,""]},"prisoner.server.webservice.PRISONER":{dispatch_request:[6,2,1,""],find_nth:[6,2,1,""],get_builder_reference:[6,2,1,""],on_begin:[6,2,1,""],on_cancel:[6,2,1,""],on_complete:[6,2,1,""],on_confirm:[6,2,1,""],on_consent:[6,2,1,""],on_fallback:[6,2,1,""],on_get_object:[6,2,1,""],on_handshake:[6,2,1,""],on_invalidate:[6,2,1,""],on_post_response:[6,2,1,""],on_publish_object:[6,2,1,""],on_register:[6,2,1,""],on_schema:[6,2,1,""],on_session_read:[6,2,1,""],on_session_timeout:[6,2,1,""],on_session_write:[6,2,1,""],render_template:[6,2,1,""],set_builder_reference:[6,2,1,""],threaded_get_object:[6,2,1,""],wsgi_app:[6,2,1,""]},"prisoner.tests":{tests:[7,0,0,"-"]},"prisoner.tests.tests":{SocialObjectsTestCase:[7,1,1,""]},"prisoner.tests.tests.SocialObjectsTestCase":{setUp:[7,2,1,""]},"prisoner.workflow":{Exceptions:[8,0,0,"-"],ExperimentBuilder:[8,0,0,"-"],PolicyProcessor:[8,0,0,"-"],SocialObjectGateway:[8,0,0,"-"],tests:[9,0,0,"-"]},"prisoner.workflow.Exceptions":{DisallowedByPrivacyPolicyError:[8,4,1,""],IncorrectSecretError:[8,4,1,""],InvalidPolicyProvidedError:[8,4,1,""],NoPrivacyPolicyProvidedError:[8,4,1,""],OperationNotImplementedError:[8,4,1,""],RuntimePrivacyPolicyParserError:[8,4,1,""],ServiceGatewayNotFoundError:[8,4,1,""],SocialObjectNotSupportedError:[8,4,1,""]},"prisoner.workflow.ExperimentBuilder":{CallbackHandler:[8,1,1,""],CompleteConsentHandler:[8,1,1,""],ConsentFlowHandler:[8,1,1,""],ExperimentBuilder:[8,1,1,""],ProviderAuthentHandler:[8,1,1,""]},"prisoner.workflow.ExperimentBuilder.CallbackHandler":{get:[8,2,1,""]},"prisoner.workflow.ExperimentBuilder.CompleteConsentHandler":{get:[8,2,1,""]},"prisoner.workflow.ExperimentBuilder.ConsentFlowHandler":{get:[8,2,1,""]},"prisoner.workflow.ExperimentBuilder.ExperimentBuilder":{authenticate_participant:[8,2,1,""],authenticate_providers:[8,2,1,""],build:[8,2,1,""],build_schema:[8,2,1,""],consent_confirmed:[8,2,1,""],get_props:[8,2,1,""],provide_contact:[8,2,1,""],provide_db_string:[8,2,1,""],provide_experimental_design:[8,2,1,""],provide_privacy_policy:[8,2,1,""],provide_title:[8,2,1,""]},"prisoner.workflow.ExperimentBuilder.ProviderAuthentHandler":{get:[8,2,1,""]},"prisoner.workflow.PolicyProcessor":{PolicyProcessor:[8,1,1,""]},"prisoner.workflow.PolicyProcessor.PolicyProcessor":{privacy_policy:[8,3,1,""],validate_policy:[8,2,1,""]},"prisoner.workflow.SocialObjectGateway":{InvalidPrivacyPolicy:[8,4,1,""],ServiceGatewayNotFound:[8,4,1,""],SocialObjectsGateway:[8,1,1,""]},"prisoner.workflow.SocialObjectGateway.SocialObjectsGateway":{GetObject:[8,2,1,""],GetObjectJSON:[8,2,1,""],PostObject:[8,2,1,""],PostObjectJSON:[8,2,1,""],cache_object:[8,2,1,""],complete_authentication:[8,2,1,""],get_participant:[8,2,1,""],get_service_gateway:[8,2,1,""],post_response:[8,2,1,""],provide_experimental_design:[8,2,1,""],provide_privacy_policy:[8,2,1,""],register_participant:[8,2,1,""],request_authentication:[8,2,1,""],restore_authentication:[8,2,1,""]},"prisoner.workflow.tests":{PolicyProcessorTests:[9,0,0,"-"],SocialObjectGatewayTests:[9,0,0,"-"]},"prisoner.workflow.tests.PolicyProcessorTests":{BasePolicyProcessorTestCase:[9,1,1,""],InferAttributesTestCase:[9,1,1,""],InferObjectTestCase:[9,1,1,""],SanitiseObjectRequestTestCase:[9,1,1,""],ValidateObjectRequestTestCase:[9,1,1,""],ValidatePolicyTestCase:[9,1,1,""]},"prisoner.workflow.tests.PolicyProcessorTests.BasePolicyProcessorTestCase":{get_bad_processor:[9,2,1,""],get_disallow_processor:[9,2,1,""],get_good_processor:[9,2,1,""],setUp:[9,2,1,""]},"prisoner.workflow.tests.PolicyProcessorTests.InferAttributesTestCase":{test_bad_attribute:[9,2,1,""],test_bad_format:[9,2,1,""],test_bad_nested_obj:[9,2,1,""],test_bad_obj:[9,2,1,""],test_good_nested_obj:[9,2,1,""],test_good_obj:[9,2,1,""]},"prisoner.workflow.tests.PolicyProcessorTests.InferObjectTestCase":{test_good_literal:[9,2,1,""],test_invalid_base:[9,2,1,""],test_invalid_literal:[9,2,1,""],test_invalid_social_gateway:[9,2,1,""],test_missing_base:[9,2,1,""],test_valid_base:[9,2,1,""],test_valid_social_gateway:[9,2,1,""]},"prisoner.workflow.tests.PolicyProcessorTests.SanitiseObjectRequestTestCase":{test_good_response:[9,2,1,""],test_logic_failOnAnd:[9,2,1,""],test_logic_failOnImplicitAnd:[9,2,1,""],test_logic_failOnNested:[9,2,1,""],test_logic_failOnOr:[9,2,1,""],test_malformed_headers:[9,2,1,""],test_malformed_response:[9,2,1,""],test_missing_headers:[9,2,1,""],test_no_allow_attribute:[9,2,1,""]},"prisoner.workflow.tests.PolicyProcessorTests.ValidateObjectRequestTestCase":{test_bad_request_badObject:[9,2,1,""],test_bad_request_badOperation:[9,2,1,""],test_fail_validation:[9,2,1,""],test_good_validation:[9,2,1,""]},"prisoner.workflow.tests.PolicyProcessorTests.ValidatePolicyTestCase":{test_bad_policy:[9,2,1,""],test_good_policy:[9,2,1,""],test_no_policy:[9,2,1,""]},"prisoner.workflow.tests.SocialObjectGatewayTests":{BaseSocialObjectGatewayTestCase:[9,1,1,""],CacheObjectTestCase:[9,1,1,""],GetObjectJSONTestCase:[9,1,1,""],ProvidePoliciesTestCase:[9,1,1,""]},"prisoner.workflow.tests.SocialObjectGatewayTests.BaseSocialObjectGatewayTestCase":{GetObject_returns_object:[9,2,1,""],ProcessorInferObject_returns_Person:[9,2,1,""],setUp:[9,2,1,""]},"prisoner.workflow.tests.SocialObjectGatewayTests.CacheObjectTestCase":{test_cache_hit:[9,2,1,""],test_cache_miss:[9,2,1,""]},"prisoner.workflow.tests.SocialObjectGatewayTests.GetObjectJSONTestCase":{test_bad_get:[9,2,1,""],test_good_get:[9,2,1,""]},"prisoner.workflow.tests.SocialObjectGatewayTests.ProvidePoliciesTestCase":{test_provide_good_exp_design:[9,2,1,""],test_provide_good_privacy_policy:[9,2,1,""],test_provide_invalid_exp_design:[9,2,1,""],test_provide_invalid_privacy_policy:[9,2,1,""]},prisoner:{SocialObjects:[2,0,0,"-"],gateway:[3,0,0,"-"],persistence:[5,0,0,"-"],server:[6,0,0,"-"],tests:[7,0,0,"-"],workflow:[8,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","attribute","Python attribute"],"4":["py","exception","Python exception"],"5":["py","function","Python function"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:attribute","4":"py:exception","5":"py:function"},terms:{"223f":6,"5343gt32":6,"__init__":3,"_friendly_nam":2,"abstract":3,"boolean":[3,8],"case":[4,7,9],"class":[2,3,4,5,6,7,8,9],"final":13,"function":[3,4,6,8,11],"int":[5,8],"long":[2,3,5,6,7],"new":[3,5,11,13],"public":8,"return":[2,3,5,6,8,13],"short":[2,3],"static":11,"true":8,"while":[0,6,13],abl:[5,8,13],about:[3,5,6,7,8,11,12,13],abov:6,accept:[0,2,3,8],access:[0,3,5,6,8,12,13],access_token:[3,8],account:[0,11,13],action:8,activ:[0,5,6,12],actor:2,actual:13,adapt:13,add:[0,5,11,13],addit:[0,2,3,6,7,8,11,13],address:[2,3,8],addresss:2,adher:3,advantag:13,affect:11,after:[3,8,11],again:[3,6],against:[5,8],agnost:13,ajax:6,album:3,albumtyp:3,all:[2,3,4,5,6,8,12],allow:[2,3,6,8,11,13],allow_mani:8,allthi:3,along:0,alongsid:[3,8],alreadi:8,also:[2,3,6,8,13],alter:2,altern:[2,12],although:13,altitud:2,alwai:3,andrew:13,ani:[0,2,3,5,6,8,11,12,13],anonym:0,anonymis:[0,2,3],anoth:2,answer:[6,13],api:[0,3,4,5,6,8,11],api_vers:3,app:[],app_id:3,app_secret:3,append:6,appli:3,applic:[2,3,8,11,13],appropri:[2,3,5,8,11,13],arbitrari:6,archiv:0,arg:[4,9],argument:[3,6,8],around:[3,8],arriv:13,artist:[3,6],ask:8,aspect:11,associ:[2,3],assum:[12,13],async:6,asynchron:6,attempt:[2,3,5,8,13],attemtp:8,attend:2,attribut:[2,3,4,6,8,11,13],audit:3,auth:3,authent:[0,2,3,4,5,6,8,9,11],authenticate_particip:8,authenticate_provid:8,author:[2,3,6,8,13],automat:[0,11,13],avail:[0,2,3,5],avoid:[2,3,12],back:8,backbon:3,backlog:3,bake:8,band:3,bar:11,base:[0,2,3,4,5,6,7,8,9],base_transform_nam:[2,3],basefacebookgatewaytestcas:4,basehandl:2,baselastfmservicegatewaytestcas:4,basepolicyprocessortestcas:9,basesocialobjectgatewaytestcas:9,basic:[3,11,14],becaus:13,been:[0,3,5,6],befor:[0,4,6,8,11,13,14],begin:[6,8],behalf:3,behav:9,between:8,bin:11,binari:2,bind:0,bio:3,biograph:[11,13],biographi:3,birthdai:[3,13],blank:6,block:[],blog:2,board:13,book:3,boot2dock:11,bootstrap:[8,11],both:[3,13],bounc:8,bound:[6,8],box:2,browser:[11,13],build:[0,3,6,8,10],build_schema:8,builder:6,built:[0,8],cach:[3,8,9],cache_object:8,cacheobjecttestcas:9,call:[0,3,4,5,6,8,13],callabl:8,callback:[3,6,8],callback_url:8,callbackhandl:8,can:[0,2,3,5,6,8,10,11,13],cannot:[6,13],categori:3,certain:6,chang:11,check:[3,5],check_non:3,checkin:3,checkintyp:3,choic:[],choos:11,circumv:3,citi:2,claus:11,clear:13,click:11,client:[3,5,6,8],clientsid:[3,5,8],clone:[],close_connect:5,coarsen:[0,2],code:[0,2,3,13],collect:[0,2,3,5,11,13],column:6,com:11,combin:[2,13],comma:6,command:[11,12],comment:[2,3,6],commit:6,common:[0,2,4],commonli:3,commun:0,complement:7,complet:[3,6,8],complete_authent:[3,8],completeconsenthandl:8,complex:8,compon:[2,3,14],concept:[],concern:0,concret:3,condit:13,confid:8,configur:12,confirm:[3,8],conflict:12,connect:[5,8],connection_str:[5,8],consent:[0,5,6,8,13],consent_confirm:8,consentflowhandl:8,consid:11,consider:0,consist:[0,2,3,5,13],constrain:11,constraint:13,construct:[2,3,8],consult:11,consum:[2,3],consumpt:8,contact:8,contain:7,content:1,context:[2,6,8],continu:[3,5,8,11],contribut:0,controlvm:11,convent:[3,7],convert:[2,3,8],cooki:[6,8],coordin:[2,8],core:3,correct:[2,8],correctli:[9,11,12],correspond:[3,5,6,8],cost:13,could:13,count:3,counterpart:[2,8],countri:2,coupl:13,cover:3,coverag:0,coverphoto:3,crawl:0,crawler:0,creat:[2,3,4,6,8,11,13],create_app:6,create_user_all_permiss:4,create_user_no_permiss:4,creation:[0,2],credenti:5,criteria:[3,6,8,13],current:[],data:[0,2,3,4,5,6,8,11,13],databas:[0,5,6,8],date:3,datetimejsonhandl:2,db_string:8,deal:3,debug:3,declar:0,decor:8,def:3,defin:13,degrad:0,deleg:9,delet:[3,4],delight:0,demo:[],demo_bootstrap:11,demonstr:[3,11,13],depend:[2,3,8,12],deploi:0,describ:13,descript:2,design:[0,2,3,5,6,8,11,13],destroi:8,destruct:2,detail:[],detect:11,determin:3,develop:[],dict:[3,4,5,8],dictat:[3,13],dictionari:[2,3,4,5,8],differ:[8,11],difficult:2,direct:0,directli:[3,5,8],directori:[7,12,13],disallowedbyprivacypolicyerror:8,dispatch_request:6,displai:[11,12,13],displaynam:[2,13],distinct:8,distribut:0,do_build_schema:5,docker:[],dockerhub:12,doe:[3,8,13],doesn:8,domain:11,don:7,done:[3,8,11],download:11,drop_first:5,durat:8,dure:[2,6,8,13],each:[2,3,6,7,8,13],earlier:11,earth:2,easiest:12,easili:13,educ:3,effect:13,either:3,element:[11,13],elementtre:[5,8],elsewher:3,email:[3,8],emb:2,embed:3,empti:6,enabl:[4,13],encod:[2,6,13],end:[2,6],endpoint:[3,4],endtim:2,enforc:13,engag:13,engin:0,ensur:[0,5,8,9,13],enter:11,entir:[3,8],entiti:3,entrypoint:8,enumer:[11,13],environ:[6,12,13],error:[6,8],escap:6,essenti:3,etc:[2,3,7,8],ethic:[0,13],evalu:[6,8],even:[2,11,13],event:[2,6],everi:[2,4],everyth:12,everywher:3,exampl:[2,3,6,8,11,13],except:1,exchang:[2,3],execut:[0,11],exist:[3,8],exp_design:[5,8],expect:[2,3,6,8,9],experi:5,experiment:[0,3,5,6,8,11,13],experimental_design:[5,8],experimentbuild:[1,5],experimentnt:6,explicitli:[3,13],expos:[2,3,6,8],express:[0,6,8],extend:3,extern:[2,3,8],extra:11,extra_arg:[3,6,8],extract:3,facebook:[],facebook_obj:3,facebookgatewai:1,facebookgatewaytest:[],facebookservicegatewai:3,factor:8,fail:8,fals:[3,5,8],familiar:[0,11,12],favourit:6,field:[3,8],file:[3,8,13],film:3,filter:[6,8],find_nth:6,first:[],firstnam:[3,13],fit:[7,8],flatten:2,flexibl:2,flow:[3,5,6,8,9],follow:[0,2,3,6,8,10,11,12,13,14],footprint:6,forc:3,form:[0,2,3,6,8,13],format:[2,3],found:[5,8],framework:0,free:2,friend:[3,13],friendli:[2,8],friendlier:[5,8],from:5,full:[0,2,3,6,8,13],fullimag:2,fundament:8,further:6,futur:[0,3,6],g43519500:6,gatewai:1,gatewaynam:3,gender:[3,11,13],gener:[0,2,3,5,8,13],generalis:13,generate_permissions_list:3,geo:3,geograph:2,get:5,get_bad_processor:[4,9],get_builder_refer:6,get_com:3,get_disallow_processor:9,get_empty_processor:4,get_existing_provider_auth:5,get_friendly_nam:[2,3],get_good_processor:[4,9],get_good_prop:4,get_graph_data:3,get_lik:3,get_particip:[5,8],get_prop:[5,8],get_service_gatewai:8,get_tabl:5,get_valu:3,getobject:[3,8],getobject_returns_object:9,getobjectjson:8,getobjectjsontestcas:9,getpermissionsforpolicytestcas:4,github:[],given:[3,4,5,6,8,11,13],good:6,gracefulli:[0,6],graph:[3,4],graphic:2,great:3,guarante:[0,3,6],guid:[11,12],guidanc:3,handl:[0,3,4,6,8,13],handler:2,handshak:6,harder:13,have:[0,2,3,6,11,12,13],haystack:[3,6],head:12,header:[3,6],height:3,held:3,help:[0,10,11,12],here:[3,11],hierarchi:13,histori:3,hometown:3,hope:3,host:8,hous:2,how:[0,3,6,8,11,13,14],howev:[3,8],http:[3,11,13],httprequest:3,hub:12,human:[2,8,13],ideal:[2,13],identifi:[0,2,3,6,8],identitfi:13,imag:[2,3,11,12,13],imagetestcas:4,immedi:6,implement:[2,3,8,11],implic:[],improv:[0,3],inaccess:2,inadvert:13,inadvertantli:13,includ:[0,2,5,6,8,12,13],incorrectli:8,incorrectsecreterror:8,indefinit:3,index:0,individu:0,inferattributestestcas:9,inferobjecttestcas:9,inform:[0,3,6,8,11,12,13],ingest:0,inherit:3,init:4,initi:[2,3,6],initialisetestcas:4,inject:[3,8],innard:8,inreplyto:[2,3,6],insert:[5,6],instal:[],instanc:[0,2,3,6,8,11,12,13],instanti:[5,8,11],instead:[5,6],instig:[3,8],intend:[0,2,3,6],interact:[3,8],interest:0,interestedin:3,interfac:[0,3,5,6,8,11],intern:[2,3,4,5,6,8],interpet:5,interpret:6,interrog:3,interv:2,intervent:[0,5],introduc:[3,13,14],invalid:[6,8],invalidpolicyprovidederror:8,invalidprivacypolici:8,invalidtransformationlevelerror:2,invok:[0,8],involv:[2,8],ioerror:[5,8],irb:13,irrecover:6,iso:[2,3],isol:12,isreadi:6,issu:0,iter:[12,13],json:[3,5,6,8],json_obj:3,jsonpickl:2,just:3,kei:[],keywarg:9,kind:[0,14],know:8,kwarg:8,label:2,lambda:[6,8],languag:[2,3],larger:6,last:[0,2,3,6,8,11],lastfm:[6,8],lastfmgatewai:1,lastfmgatewaytest:[],lastfmservicegatewai:3,lastnam:[3,13],lat:2,later:[6,11,13],latest:12,latitud:2,launch:11,layer:6,learn:11,let:[3,8,11],level:[2,3],lhutton:[11,12],librari:[],life:2,lifecycl:8,lightweight:[3,6],like:[0,3],limit:3,line:[11,12],link:[2,3],linux:11,list:[2,3,6,8],liter:8,literatur:3,live:7,lng:2,load:3,local:[],localhost:[11,12],locat:[2,3],logic:[2,7,8],longer:0,longev:0,longitud:2,look:[3,11],lookup:6,love:3,lukeweb:8,machin:12,made:[3,8],mai:[2,3,6,8,12],mail:2,main:2,mainli:3,maintain:[0,3,8],make:[2,3,5,6,8,11,12,13],manag:[5,6,8],mandatori:3,mani:8,manual:11,map:[0,2,3,11,12],mapped_port:12,markup:2,match:[3,6,13],maximum:2,maybeattend:2,mean:[3,13],meaning:8,mechan:[3,8],memori:6,messag:[2,12],meta_t:5,metadata:[0,3,5],method:[3,8,11],methodnam:[4,7,9],microblog:2,middl:3,middlenam:[3,13],might:[2,8],minut:12,miss:[8,11],mobil:3,modif:11,modifi:[],modul:1,more:[8,12,13],most:[2,3],movi:3,much:7,multi:6,multipl:[],music:3,must:[2,3,4,5,6,8,13],name:[2,3,5,8,11,12],namespac:[8,13],nativ:[8,11],natpf1:11,natur:[2,13],navig:11,necessari:[3,8,13],need:[0,3,8,11,13],needl:[3,6],nest:8,network:[0,3,13],newer:0,next:[11,12],non:2,none:[3,5,6,8],noprivacypolicyprovidederror:8,notattend:2,note:[2,3,6,8,11],now:[11,12,13],number:[2,3],obj:2,object:[2,3,4,5,6,8,9,11,13],object_id:3,object_nam:6,object_to_cach:8,object_typ:[3,8],objecttyp:3,occur:2,off:[],offlin:13,offset:3,often:2,old:3,older:0,on_begin:6,on_cancel:6,on_complet:6,on_confirm:6,on_cons:6,on_fallback:6,on_get:11,on_get_object:6,on_handshak:6,on_invalid:6,on_object:13,on_post_respons:6,on_publish_object:6,on_regist:6,on_schema:6,on_session_read:6,on_session_timeout:6,on_session_writ:6,onc:[3,8],onli:[0,3,6,8,13],onlin:2,onward:6,openli:12,oper:[3,8],operationnotimplementederror:8,option:[3,8],order:3,org:13,orient:3,origin:[3,5,6,8],other:[0,3,8,10,11,13,14],otherwis:[3,5],our:[6,11,12,13],outgo:8,outlin:13,outsid:13,own:[2,3,6,7,8],pack:2,packag:1,page:[0,3,11],param:[3,4,5,8],paramet:[2,3,4,5,6,8],pars:[3,5,8],parse_com:3,parse_json:3,parse_lik:3,parse_loc:3,parse_tag:3,part:3,parti:8,particip:[0,3,5,6,8,13],participant_id:[5,8],particularli:8,pass:[3,6,8],past:11,path:[3,4,5,8],pattern:6,payload:[3,6,8],peopl:[2,3],per:8,perform:[3,4,6,8],period:6,permalink:[2,3],permament:2,perman:[2,6],permiss:[3,4,11],persist:1,persistencemanag:1,person:[2,3,8],perspect:13,photo:[2,3,8],physic:2,pictur:3,pip:12,pipe:8,pixel:3,pixi:6,place:[2,3,8,13],plain:[2,8],platform:[11,13],playlist:3,pleas:[0,11],point:[2,6],polici:5,policy_processor:5,policydocumentgener:1,policyprocessor:1,policyprocessortest:[],polit:[3,11],politicalview:[3,11],popul:[3,13],port:[11,12],porta:[],portal:3,posit:[2,3],position_as_dict:2,possibl:[2,3,5],post:[2,3,4,6,8],post_graph_data:[3,4],post_respons:[5,8],post_response_json:5,postal:2,postalcod:2,postobject:8,postobjectjson:8,potenti:3,practic:13,pre:[],prefer:3,prefix:[8,13],prepar:12,prerequisit:[],present:8,previou:[3,6],previous:[3,5],primari:6,print:2,prisess:6,prisoner_id:[5,6,8],privaci:5,privacy_polici:[8,13],probabl:[0,12],problem:0,proce:8,process:[3,8,11,13],processor:8,processorinferobject_returns_person:9,profil:[3,6,11,13],progress:0,prompt:11,prop:[3,4,5],properti:2,protocol:13,provid:[2,3,5,6,8,11,13],provide_contact:8,provide_db_str:8,provide_experimental_design:8,provide_privacy_polici:8,provide_titl:8,providepoliciestestcas:9,providerauthenthandl:8,publish:[0,2,3,4,6,8,13],pull:[0,12],push:[8,12],put:8,pylast:3,python:[8,12,13],queri:[3,4,6,8],question:[6,13],quick:11,quickest:[],quickli:12,rais:[0,2,5,8],rang:[2,3],rather:[8,11,12],read:[3,6,8,14],readabl:[2,6,8,13],readi:[0,6],reauthent:5,rebuild_engin:5,receiv:[3,5,6,8],recommend:[10,12,14],recov:6,redirect:[3,8],reduc:2,refer:[0,5,8],reflect:13,refresh:3,region:2,regist:[3,5,6,8,11,13],register_particip:[5,8],register_participant_with_provid:5,registri:12,relat:[2,3,6,8],relationship:3,relationshipstatu:3,releas:[0,12],relev:[2,4,5,8],religion:[3,11],remov:6,render:8,render_templ:6,replac:3,repli:[2,3],replic:13,repositori:12,repres:[2,3],represent:[2,3,8,13],reproduc:[0,10,13],request:[0,3,5,6,8,9,11,13],request_authent:[3,8],request_handl:3,requesthandl:8,requir:[0,3,5,6,8,12,13],requisit:[],requst_authent:8,research:[0,8,13],resolv:12,resourc:[2,3],respond:2,respons:[0,2,3,5,6,8],rest:[3,6,8],restart:6,restor:[2,3],restore_authent:[3,8],result:[3,6,11],retain:6,retreiv:3,retriev:[2,3,5,6,8,11,13],review:[8,11,13],revisit:11,rich:2,role:11,row:5,rsvp:2,rule:[0,13],run:7,runner:7,runtest:[4,7,9],runtim:13,runtimeprivacypolicyparsererror:8,safe:6,sai:2,said:3,same:[3,6,8,13],sanitis:[0,2,3,5,8,13],sanitiseobjectrequesttestcas:9,sarhead:3,satisfi:0,scema:5,schema:[5,6,8],schemaloc:13,scheme:3,scope:8,scrape:0,screen:11,script:11,search:0,second:[3,8],secret:[8,11],section:11,see:[3,7,8,11,12],seen:11,segreg:7,self:[2,3,11],semant:[2,8],sens:2,sensit:[0,8,13],sentenc:[2,8],seper:6,serial:2,server:[1,5],server_url:8,servic:[0,2,3,5,6,7,8,9,11,13],servicegatewai:1,servicegatewaynotfound:8,servicegatewaynotfounderror:8,session:[3,5,6,8,11,13],set:[2,3,4,6,11,12,13],set_builder_refer:6,set_test_user_attribut:4,setup:[4,7,9],sever:[2,12],sexual:3,sha224:2,share:[2,13],shorter:2,should:[2,3,5,6,8,11,12],shout:3,show:[11,13],side:[3,5],signal:5,signatur:3,signific:[3,11],significantoth:3,similar:[3,8],similarli:[8,11],simpl:[0,6,10,13],simpli:[3,13],simplic:[],simplifi:0,singl:[0,8],site:[0,3,11,13],size:[2,3],skip:11,small:[2,11],social:[0,2,3,5,6,8,13],social_object:3,socialactivityrespons:3,socialgatewaytest:[],socialobject:1,socialobjectgatewai:1,socialobjectgatewaytest:[],socialobjectnotsupportederror:8,socialobjectsgatewai:[5,8],socialobjectstestcas:7,sog:[5,8],some:[4,8,11,13],someon:[3,8],somewher:3,speak:3,spec:8,specialis:[2,3],specif:[3,13],specifi:[3,8],spin:[],sqlalchemi:0,stabil:12,stage:[3,8],standard:[2,3,13],standardis:13,start:[],start_respons:6,starttim:2,state:[2,6,8],statu:[2,3],status:3,statuslist:3,statustestcas:4,steer:0,step:[6,8,11],still:3,storag:5,store:[0,3,5,6,8,13],str:[2,3,4,5,8],str_to_tim:3,strategi:13,street:2,streetaddress:2,string:[2,3,6,8],strongli:[10,12],stub:3,studi:[0,13],subclass:[2,3],subject:[5,8],submodul:1,subpackag:1,subsequ:[6,8],subset:8,succes:3,success:[3,8],successfulli:5,suggest:0,suit:[7,9],suitabl:3,summari:13,superclass:3,suppli:[3,8],support:[0,2,3,13,14],sure:[11,12],surfac:3,syntax:[0,8],system:[0,12],table_nam:5,table_typ:5,tag:[2,3,8,12],take:[3,8,11,12],target:3,tast:3,tcp:11,template_nam:6,temporari:[6,8],temporarili:6,term:2,test:1,test_bad_attribut:9,test_bad_format:9,test_bad_get:9,test_bad_nested_obj:9,test_bad_obj:9,test_bad_polici:[4,9],test_bad_prop:4,test_bad_request_badobject:9,test_bad_request_badoper:9,test_bad_token:4,test_cache_hit:9,test_cache_miss:9,test_fail_valid:9,test_get_failur:4,test_get_success:4,test_good_get:[4,9],test_good_liter:9,test_good_nested_obj:9,test_good_obj:9,test_good_polici:[4,9],test_good_prop:4,test_good_respons:9,test_good_token:4,test_good_valid:9,test_invalid_bas:9,test_invalid_liter:9,test_invalid_social_gatewai:9,test_logic_failonand:9,test_logic_failonimplicitand:9,test_logic_failonnest:9,test_logic_failonor:9,test_malformed_head:9,test_malformed_respons:9,test_missing_bas:9,test_missing_head:9,test_no_allow_attribut:9,test_no_polici:[4,9],test_no_prop:4,test_no_token:4,test_post:4,test_provide_good_exp_design:9,test_provide_good_privacy_polici:9,test_provide_invalid_exp_design:9,test_provide_invalid_privacy_polici:9,test_valid_bas:9,test_valid_social_gatewai:9,testcas:[4,7,9],text:[2,8],textual:[2,3],than:[2,8,12,13],thei:[0,2,3,7,8,13],them:[0,3,5,8],themselv:[3,8,13],therefor:13,thi:5,those:13,threaded_get_object:6,three:[3,10,13],through:[3,5,6,8,11],throughout:[3,8],thu:3,thumb:0,thumbnail:3,time:[2,3],timelin:3,timezon:3,titl:[3,8],todo:11,token:[3,4,5,6,8],too:7,tool:0,top:11,tornado:8,town:2,track:[0,3,6],trade:[],transform:[2,3],transform_artist:3,transform_hash:2,transform_reduc:2,transpar:3,tri:11,trivial:[0,11],tupl:5,turn:[8,11],tutori:[],tweet:[3,13],twitter:[0,3],twittergatewai:1,twitterservicegatewai:3,two:[3,8,12],txt:12,type:[2,3,5,6,8,11,13],typic:3,uid:3,under:[0,13],underli:[12,13],understand:[2,8,11,14],unescap:8,uniqu:[2,3,8],unit:7,unittest:[4,7,9],unnecessari:[],until:13,updat:[2,3,4],updatedtim:3,upload:[2,3],uri:[2,3],url:[2,3,6,8,11],usabl:8,user:[0,3,4,6,8,11,13],usernam:[3,13],usertestcas:4,usr:11,usual:[3,6,8],utc:3,utf:13,util:0,valid:[3,5,6,8],validate_design:5,validate_polici:8,validateobjectrequesttestcas:9,validatepolicytestcas:9,valu:[2,3,4,6,8],vboxmanag:11,verifi:8,version:[0,2,3,6,8,13],via:[0,3,12],video:2,villag:2,violat:13,virtual:12,virtualbox:11,virtualenv:12,visibl:11,visit:[3,6,8,11,12],visual:2,wai:[3,8,11,12],wall:3,want:[6,12,13],web:[5,6,8,11,13],webservic:1,websit:11,well:[3,8],were:3,werkzeug:8,whatev:8,when:[2,3,6,8,11],where:[0,2,3,5,6,7,8,12,13],wherea:8,whether:[3,5],which:[0,2,3,6,8,11,12,13],whitelist:11,who:[2,3,4],who_for:8,whose:[3,6],why:11,width:3,wildcard:6,wish:13,within:[3,12],without:[2,6,8,12],word:2,work:[3,11,12,14],workflow:1,worri:[7,12],would:0,wrap:[0,3],wrapped_head:3,wrappedrespons:3,wrapper:[3,5,8],write:5,written:13,wrote:2,wsgi:12,wsgi_app:6,www:13,xml:[5,8,11,13],xmln:13,xmlschema:13,xsd:13,xsi:13,yet:[0,6],yield:13,you:[0,3,6,7,8,10,11,12,13],your:7,yourself:8,yyyi:3,zip:2},titles:["PRISONER","&lt;no title&gt;","prisoner package","prisoner.gateway package","prisoner.gateway.tests package","prisoner.persistence package","prisoner.server package","prisoner.tests package","prisoner.workflow package","prisoner.workflow.tests package","Tutorials","Running the PRISONER demo","Installing PRISONER","Writing your first experiment","Key concepts"],titleterms:{app:11,clone:12,concept:14,contain:11,content:[2,3,4,5,6,7,8,9],current:0,demo:11,develop:[0,12],docker:[11,12],document:[],except:8,experi:13,experimentbuild:8,facebook:11,facebookgatewai:3,facebookgatewaytest:4,featur:0,first:13,from:12,gatewai:[3,4],get:[],github:12,indic:0,instal:12,kei:14,lastfmgatewai:3,lastfmgatewaytest:4,local:12,modifi:11,modul:[2,3,4,5,6,7,8,9],packag:[2,3,4,5,6,7,8,9],persist:5,persistencemanag:5,polici:13,policydocumentgener:8,policyprocessor:8,policyprocessortest:9,pre:[],prerequisit:[11,13],prison:[0,2,3,4,5,6,7,8,9,11,12],privaci:13,quickest:[],requisit:[],run:11,server:6,servicegatewai:3,socialgatewaytest:4,socialobject:2,socialobjectgatewai:8,socialobjectgatewaytest:9,spin:12,start:11,submodul:[2,3,4,5,6,7,8,9],subpackag:[2,3,8],tabl:0,test:[4,7,9],thi:13,tutori:[10,13],twittergatewai:3,webservic:6,welcom:[],what:0,workflow:[8,9],write:13,your:13}})