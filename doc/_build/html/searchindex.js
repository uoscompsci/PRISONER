Search.setIndex({envversion:46,filenames:["index","modules","prisoner","prisoner.gateway","prisoner.gateway.tests","prisoner.persistence","prisoner.server","prisoner.tests","prisoner.workflow","prisoner.workflow.tests","tutorials","tutorials.gettingstarted","tutorials.helloworld","tutorials.keyconcepts"],objects:{"":{prisoner:[2,0,0,"-"]},"prisoner.SocialObjects":{Address:[2,1,1,""],Collection:[2,1,1,""],Comment:[2,1,1,""],DateTimeJSONHandler:[2,1,1,""],Event:[2,1,1,""],Image:[2,1,1,""],InvalidTransformationLevelError:[2,4,1,""],Note:[2,1,1,""],Person:[2,1,1,""],Place:[2,1,1,""],SocialObject:[2,1,1,""]},"prisoner.SocialObjects.Address":{country:[2,3,1,""],formatted:[2,3,1,""],locality:[2,3,1,""],postalCode:[2,3,1,""],region:[2,3,1,""],streetAddress:[2,3,1,""]},"prisoner.SocialObjects.Collection":{objects:[2,3,1,""]},"prisoner.SocialObjects.Comment":{inReplyTo:[2,3,1,""]},"prisoner.SocialObjects.DateTimeJSONHandler":{flatten:[2,2,1,""],restore:[2,2,1,""]},"prisoner.SocialObjects.Event":{attending:[2,3,1,""],endTime:[2,3,1,""],maybeAttending:[2,3,1,""],notAttending:[2,3,1,""],startTime:[2,3,1,""]},"prisoner.SocialObjects.Image":{fullImage:[2,3,1,""]},"prisoner.SocialObjects.Person":{image:[2,3,1,""]},"prisoner.SocialObjects.Place":{address:[2,3,1,""],position:[2,3,1,""],position_as_dict:[2,2,1,""]},"prisoner.SocialObjects.SocialObject":{author:[2,3,1,""],base_transform_name:[2,2,1,""],content:[2,3,1,""],displayName:[2,3,1,""],get_friendly_name:[2,2,1,""],id:[2,3,1,""],location:[2,3,1,""],provider:[2,3,1,""],published:[2,3,1,""],tags:[2,3,1,""],transform_hash:[2,2,1,""],transform_reduce:[2,2,1,""],updated:[2,3,1,""],url:[2,3,1,""]},"prisoner.gateway":{FacebookGateway:[3,0,0,"-"],LastfmGateway:[3,0,0,"-"],ServiceGateway:[3,0,0,"-"],TwitterGateway:[3,0,0,"-"],tests:[4,0,0,"-"]},"prisoner.gateway.FacebookGateway":{Album:[3,1,1,""],Albums:[3,1,1,""],Book:[3,1,1,""],Checkin:[3,1,1,""],Checkins:[3,1,1,""],Comment:[3,1,1,""],Comments:[3,1,1,""],FacebookServiceGateway:[3,1,1,""],Friends:[3,1,1,""],Like:[3,1,1,""],Likes:[3,1,1,""],Movie:[3,1,1,""],Music:[3,1,1,""],Page:[3,1,1,""],Photo:[3,1,1,""],Photos:[3,1,1,""],Status:[3,1,1,""],StatusList:[3,1,1,""],Tags:[3,1,1,""],User:[3,1,1,""],check_none:[3,5,1,""]},"prisoner.gateway.FacebookGateway.Album":{albumType:[3,3,1,""],comments:[3,3,1,""],count:[3,3,1,""],coverPhoto:[3,3,1,""],likes:[3,3,1,""],photos:[3,3,1,""],privacy:[3,3,1,""]},"prisoner.gateway.FacebookGateway.Checkin":{checkinType:[3,3,1,""],image:[3,3,1,""]},"prisoner.gateway.FacebookGateway.FacebookServiceGateway":{Album:[3,2,1,""],Book:[3,2,1,""],Checkin:[3,2,1,""],Friends:[3,2,1,""],Like:[3,2,1,""],Movie:[3,2,1,""],Music:[3,2,1,""],Photo:[3,2,1,""],Session:[3,2,1,""],Status:[3,2,1,""],User:[3,2,1,""],complete_authentication:[3,2,1,""],generate_permissions_list:[3,2,1,""],get_comments:[3,2,1,""],get_graph_data:[3,2,1,""],get_likes:[3,2,1,""],get_value:[3,2,1,""],parse_comments:[3,2,1,""],parse_json:[3,2,1,""],parse_likes:[3,2,1,""],parse_location:[3,2,1,""],parse_tags:[3,2,1,""],post_graph_data:[3,2,1,""],request_authentication:[3,2,1,""],request_handler:[3,2,1,""],restore_authentication:[3,2,1,""],str_to_time:[3,2,1,""]},"prisoner.gateway.FacebookGateway.Page":{category:[3,3,1,""],image:[3,3,1,""]},"prisoner.gateway.FacebookGateway.Photo":{comments:[3,3,1,""],height:[3,3,1,""],image:[3,3,1,""],likes:[3,3,1,""],position:[3,3,1,""],tags:[3,3,1,""],thumbnail:[3,3,1,""],width:[3,3,1,""]},"prisoner.gateway.FacebookGateway.Status":{comments:[3,3,1,""],likes:[3,3,1,""],link:[3,3,1,""],privacy:[3,3,1,""]},"prisoner.gateway.FacebookGateway.User":{bio:[3,3,1,""],birthday:[3,3,1,""],education:[3,3,1,""],email:[3,3,1,""],firstName:[3,3,1,""],gender:[3,3,1,""],hometown:[3,3,1,""],interestedIn:[3,3,1,""],languages:[3,3,1,""],lastName:[3,3,1,""],location:[3,3,1,""],middleName:[3,3,1,""],politicalViews:[3,3,1,""],relationshipStatus:[3,3,1,""],religion:[3,3,1,""],significantOther:[3,3,1,""],timezone:[3,3,1,""],updatedTime:[3,3,1,""],username:[3,3,1,""],work:[3,3,1,""]},"prisoner.gateway.LastfmGateway":{LastfmServiceGateway:[3,1,1,""],Playlist:[3,1,1,""],Track:[3,1,1,""]},"prisoner.gateway.LastfmGateway.LastfmServiceGateway":{Comment:[3,2,1,""],Image:[3,2,1,""],Playlist:[3,2,1,""],Session:[3,2,1,""],Track:[3,2,1,""],complete_authentication:[3,2,1,""],request_authentication:[3,2,1,""],restore_authentication:[3,2,1,""]},"prisoner.gateway.LastfmGateway.Track":{artist:[3,3,1,""],get_friendly_name:[3,2,1,""],tag:[3,3,1,""],title:[3,3,1,""],transform_artist:[3,2,1,""]},"prisoner.gateway.ServiceGateway":{SARHeaders:[3,1,1,""],ServiceGateway:[3,1,1,""],SocialActivityResponse:[3,1,1,""],WrappedResponse:[3,1,1,""]},"prisoner.gateway.ServiceGateway.SARHeaders":{object_type:[3,3,1,""],operation:[3,3,1,""],payload:[3,3,1,""],provider:[3,3,1,""],wrapped_headers:[3,3,1,""]},"prisoner.gateway.ServiceGateway.ServiceGateway":{Image:[3,2,1,""],Session:[3,2,1,""],complete_authentication:[3,2,1,""],request_authentication:[3,2,1,""],request_handler:[3,2,1,""],restore_authentication:[3,2,1,""]},"prisoner.gateway.ServiceGateway.SocialActivityResponse":{content:[3,3,1,""],headers:[3,3,1,""]},"prisoner.gateway.ServiceGateway.WrappedResponse":{headers:[3,3,1,""],social_object:[3,3,1,""]},"prisoner.gateway.TwitterGateway":{Timeline:[3,1,1,""],TwitterServiceGateway:[3,1,1,""]},"prisoner.gateway.TwitterGateway.Timeline":{id:[3,3,1,""]},"prisoner.gateway.TwitterGateway.TwitterServiceGateway":{Session:[3,2,1,""],Timeline:[3,2,1,""],complete_authentication:[3,2,1,""],request_authentication:[3,2,1,""]},"prisoner.gateway.tests":{FacebookGatewayTests:[4,0,0,"-"],LastfmGatewayTests:[4,0,0,"-"]},"prisoner.gateway.tests.FacebookGatewayTests":{BaseFacebookGatewayTestCase:[4,1,1,""],GetPermissionsForPolicyTestCase:[4,1,1,""],InitialiseTestCase:[4,1,1,""],StatusTestCase:[4,1,1,""],UserTestCase:[4,1,1,""]},"prisoner.gateway.tests.FacebookGatewayTests.BaseFacebookGatewayTestCase":{create_user_all_permissions:[4,2,1,""],create_user_no_permissions:[4,2,1,""],get_bad_processor:[4,2,1,""],get_empty_processor:[4,2,1,""],get_good_processor:[4,2,1,""],get_good_props:[4,2,1,""],post_graph_data:[4,2,1,""],setUp:[4,2,1,""],set_test_user_attributes:[4,2,1,""]},"prisoner.gateway.tests.FacebookGatewayTests.GetPermissionsForPolicyTestCase":{test_bad_policy:[4,2,1,""],test_good_policy:[4,2,1,""]},"prisoner.gateway.tests.FacebookGatewayTests.InitialiseTestCase":{test_bad_policy:[4,2,1,""],test_bad_props:[4,2,1,""],test_bad_token:[4,2,1,""],test_good_policy:[4,2,1,""],test_good_props:[4,2,1,""],test_good_token:[4,2,1,""],test_no_policy:[4,2,1,""],test_no_props:[4,2,1,""],test_no_token:[4,2,1,""]},"prisoner.gateway.tests.FacebookGatewayTests.StatusTestCase":{test_post:[4,2,1,""]},"prisoner.gateway.tests.FacebookGatewayTests.UserTestCase":{test_good_get:[4,2,1,""],test_post:[4,2,1,""]},"prisoner.gateway.tests.LastfmGatewayTests":{BaseLastfmServiceGatewayTestCase:[4,1,1,""],ImageTestCase:[4,1,1,""]},"prisoner.gateway.tests.LastfmGatewayTests.BaseLastfmServiceGatewayTestCase":{setUp:[4,2,1,""]},"prisoner.gateway.tests.LastfmGatewayTests.ImageTestCase":{test_get_failure:[4,2,1,""],test_get_success:[4,2,1,""]},"prisoner.persistence":{PersistenceManager:[5,0,0,"-"]},"prisoner.persistence.PersistenceManager":{PersistenceManager:[5,1,1,""]},"prisoner.persistence.PersistenceManager.PersistenceManager":{close_connection:[5,2,1,""],do_build_schema:[5,2,1,""],experimental_design:[5,3,1,""],get_existing_provider_auth:[5,2,1,""],get_participant:[5,2,1,""],get_props:[5,2,1,""],get_table:[5,2,1,""],post_response:[5,2,1,""],post_response_json:[5,2,1,""],props:[5,3,1,""],rebuild_engine:[5,2,1,""],register_participant:[5,2,1,""],register_participant_with_provider:[5,2,1,""],validate_design:[5,2,1,""]},"prisoner.server":{webservice:[6,0,0,"-"]},"prisoner.server.webservice":{PRISONER:[6,1,1,""],create_app:[6,5,1,""]},"prisoner.server.webservice.PRISONER":{dispatch_request:[6,2,1,""],find_nth:[6,2,1,""],get_builder_reference:[6,2,1,""],on_begin:[6,2,1,""],on_cancel:[6,2,1,""],on_complete:[6,2,1,""],on_confirm:[6,2,1,""],on_consent:[6,2,1,""],on_fallback:[6,2,1,""],on_get_object:[6,2,1,""],on_handshake:[6,2,1,""],on_invalidate:[6,2,1,""],on_post_response:[6,2,1,""],on_publish_object:[6,2,1,""],on_register:[6,2,1,""],on_schema:[6,2,1,""],on_session_read:[6,2,1,""],on_session_timeout:[6,2,1,""],on_session_write:[6,2,1,""],render_template:[6,2,1,""],set_builder_reference:[6,2,1,""],threaded_get_object:[6,2,1,""],wsgi_app:[6,2,1,""]},"prisoner.tests":{tests:[7,0,0,"-"]},"prisoner.tests.tests":{SocialObjectsTestCase:[7,1,1,""]},"prisoner.tests.tests.SocialObjectsTestCase":{setUp:[7,2,1,""]},"prisoner.workflow":{Exceptions:[8,0,0,"-"],ExperimentBuilder:[8,0,0,"-"],PolicyProcessor:[8,0,0,"-"],SocialObjectGateway:[8,0,0,"-"],tests:[9,0,0,"-"]},"prisoner.workflow.Exceptions":{DisallowedByPrivacyPolicyError:[8,4,1,""],IncorrectSecretError:[8,4,1,""],InvalidPolicyProvidedError:[8,4,1,""],NoPrivacyPolicyProvidedError:[8,4,1,""],OperationNotImplementedError:[8,4,1,""],RuntimePrivacyPolicyParserError:[8,4,1,""],ServiceGatewayNotFoundError:[8,4,1,""],SocialObjectNotSupportedError:[8,4,1,""]},"prisoner.workflow.ExperimentBuilder":{CallbackHandler:[8,1,1,""],CompleteConsentHandler:[8,1,1,""],ConsentFlowHandler:[8,1,1,""],ExperimentBuilder:[8,1,1,""],ProviderAuthentHandler:[8,1,1,""]},"prisoner.workflow.ExperimentBuilder.CallbackHandler":{get:[8,2,1,""]},"prisoner.workflow.ExperimentBuilder.CompleteConsentHandler":{get:[8,2,1,""]},"prisoner.workflow.ExperimentBuilder.ConsentFlowHandler":{get:[8,2,1,""]},"prisoner.workflow.ExperimentBuilder.ExperimentBuilder":{authenticate_participant:[8,2,1,""],authenticate_providers:[8,2,1,""],build:[8,2,1,""],build_schema:[8,2,1,""],consent_confirmed:[8,2,1,""],get_props:[8,2,1,""],provide_contact:[8,2,1,""],provide_db_string:[8,2,1,""],provide_experimental_design:[8,2,1,""],provide_privacy_policy:[8,2,1,""],provide_title:[8,2,1,""]},"prisoner.workflow.ExperimentBuilder.ProviderAuthentHandler":{get:[8,2,1,""]},"prisoner.workflow.PolicyProcessor":{PolicyProcessor:[8,1,1,""]},"prisoner.workflow.PolicyProcessor.PolicyProcessor":{privacy_policy:[8,3,1,""],validate_policy:[8,2,1,""]},"prisoner.workflow.SocialObjectGateway":{InvalidPrivacyPolicy:[8,4,1,""],ServiceGatewayNotFound:[8,4,1,""],SocialObjectsGateway:[8,1,1,""]},"prisoner.workflow.SocialObjectGateway.SocialObjectsGateway":{GetObject:[8,2,1,""],GetObjectJSON:[8,2,1,""],PostObject:[8,2,1,""],PostObjectJSON:[8,2,1,""],cache_object:[8,2,1,""],complete_authentication:[8,2,1,""],get_participant:[8,2,1,""],get_service_gateway:[8,2,1,""],post_response:[8,2,1,""],provide_experimental_design:[8,2,1,""],provide_privacy_policy:[8,2,1,""],register_participant:[8,2,1,""],request_authentication:[8,2,1,""],restore_authentication:[8,2,1,""]},"prisoner.workflow.tests":{PolicyProcessorTests:[9,0,0,"-"],SocialObjectGatewayTests:[9,0,0,"-"]},"prisoner.workflow.tests.PolicyProcessorTests":{BasePolicyProcessorTestCase:[9,1,1,""],InferAttributesTestCase:[9,1,1,""],InferObjectTestCase:[9,1,1,""],SanitiseObjectRequestTestCase:[9,1,1,""],ValidateObjectRequestTestCase:[9,1,1,""],ValidatePolicyTestCase:[9,1,1,""]},"prisoner.workflow.tests.PolicyProcessorTests.BasePolicyProcessorTestCase":{get_bad_processor:[9,2,1,""],get_disallow_processor:[9,2,1,""],get_good_processor:[9,2,1,""],setUp:[9,2,1,""]},"prisoner.workflow.tests.PolicyProcessorTests.InferAttributesTestCase":{test_bad_attribute:[9,2,1,""],test_bad_format:[9,2,1,""],test_bad_nested_obj:[9,2,1,""],test_bad_obj:[9,2,1,""],test_good_nested_obj:[9,2,1,""],test_good_obj:[9,2,1,""]},"prisoner.workflow.tests.PolicyProcessorTests.InferObjectTestCase":{test_good_literal:[9,2,1,""],test_invalid_base:[9,2,1,""],test_invalid_literal:[9,2,1,""],test_invalid_social_gateway:[9,2,1,""],test_missing_base:[9,2,1,""],test_valid_base:[9,2,1,""],test_valid_social_gateway:[9,2,1,""]},"prisoner.workflow.tests.PolicyProcessorTests.SanitiseObjectRequestTestCase":{test_good_response:[9,2,1,""],test_logic_failOnAnd:[9,2,1,""],test_logic_failOnImplicitAnd:[9,2,1,""],test_logic_failOnNested:[9,2,1,""],test_logic_failOnOr:[9,2,1,""],test_malformed_headers:[9,2,1,""],test_malformed_response:[9,2,1,""],test_missing_headers:[9,2,1,""],test_no_allow_attribute:[9,2,1,""]},"prisoner.workflow.tests.PolicyProcessorTests.ValidateObjectRequestTestCase":{test_bad_request_badObject:[9,2,1,""],test_bad_request_badOperation:[9,2,1,""],test_fail_validation:[9,2,1,""],test_good_validation:[9,2,1,""]},"prisoner.workflow.tests.PolicyProcessorTests.ValidatePolicyTestCase":{test_bad_policy:[9,2,1,""],test_good_policy:[9,2,1,""],test_no_policy:[9,2,1,""]},"prisoner.workflow.tests.SocialObjectGatewayTests":{BaseSocialObjectGatewayTestCase:[9,1,1,""],CacheObjectTestCase:[9,1,1,""],GetObjectJSONTestCase:[9,1,1,""],ProvidePoliciesTestCase:[9,1,1,""]},"prisoner.workflow.tests.SocialObjectGatewayTests.BaseSocialObjectGatewayTestCase":{GetObject_returns_object:[9,2,1,""],ProcessorInferObject_returns_Person:[9,2,1,""],setUp:[9,2,1,""]},"prisoner.workflow.tests.SocialObjectGatewayTests.CacheObjectTestCase":{test_cache_hit:[9,2,1,""],test_cache_miss:[9,2,1,""]},"prisoner.workflow.tests.SocialObjectGatewayTests.GetObjectJSONTestCase":{test_bad_get:[9,2,1,""],test_good_get:[9,2,1,""]},"prisoner.workflow.tests.SocialObjectGatewayTests.ProvidePoliciesTestCase":{test_provide_good_exp_design:[9,2,1,""],test_provide_good_privacy_policy:[9,2,1,""],test_provide_invalid_exp_design:[9,2,1,""],test_provide_invalid_privacy_policy:[9,2,1,""]},prisoner:{SocialObjects:[2,0,0,"-"],gateway:[3,0,0,"-"],persistence:[5,0,0,"-"],server:[6,0,0,"-"],tests:[7,0,0,"-"],workflow:[8,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","attribute","Python attribute"],"4":["py","exception","Python exception"],"5":["py","function","Python function"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:attribute","4":"py:exception","5":"py:function"},terms:{"223f":6,"5343gt32":6,"__init__":3,"_friendly_nam":2,"abstract":3,"boolean":[3,8],"case":[4,7,9],"class":[2,3,4,5,6,7,8,9],"final":12,"function":[3,4,6,8],"int":[5,8],"long":[2,3,5,6,7],"new":[3,5],"public":8,"return":[2,3,5,6,8],"short":[2,3],"true":8,"while":[0,6,12],abl:[5,8,12],about:[3,5,6,7,8,11],abov:6,accept:[0,2,3,8],access:[0,3,5,6,8,11],access_token:[3,8],account:[0,12],action:8,activ:[0,5,6,11],actor:2,actual:12,adapt:12,add:[0,5],addit:[0,2,3,6,7,8],address:[2,3,8],addresss:2,adher:3,advantag:12,after:[3,8],again:[3,6],against:[5,8],agnost:12,ajax:6,album:3,albumtyp:3,all:[2,3,4,5,6,8,11],allow:[2,3,6,8,12],allow_mani:8,allthi:3,along:0,alongsid:[3,8],alreadi:8,also:[2,3,6,8],alter:2,altern:[2,11],altitud:2,alwai:3,ani:[0,2,3,5,6,8,11,12],anonym:0,anonymis:[0,2,3],anoth:2,answer:[6,12],api:[0,3,4,5,6,8],app:3,append:6,appli:3,applic:[2,3,8,12],appropri:[2,3,5,8,12],arbitrari:6,archiv:0,arg:[4,9],argument:[3,6,8],around:[3,8],arriv:12,artist:[3,6],ask:8,associ:[2,3],assum:[11,12],async:6,asynchron:6,attempt:[2,3,5,8,12],attemtp:8,attend:2,attribut:[2,3,4,6,8,12],audit:3,auth:3,authent:[0,2,3,4,5,6,8,9],authenticate_particip:8,authenticate_provid:8,author:[2,3,6,8],automat:[0,12],avail:[0,2,3,5],avoid:[2,3,11],back:8,backbon:3,backlog:3,bake:8,band:3,base:[0,2,3,4,5,6,7,8,9],base_transform_nam:[2,3],basefacebookgatewaytestcas:4,basehandl:2,baselastfmservicegatewaytestcas:4,basepolicyprocessortestcas:9,basesocialobjectgatewaytestcas:9,basic:[3,13],been:[0,3,5,6],befor:[0,4,6,8,12,13],begin:[6,8],behalf:3,behav:9,between:8,binari:2,bind:0,bio:3,biographi:3,birthdai:3,blank:6,blog:2,board:12,book:3,bootstrap:8,both:[3,12],bounc:8,bound:[6,8],box:2,browser:12,build:[0,3,6,8,10],build_schema:8,builder:6,built:[0,8],cach:[3,8,9],cache_object:8,cacheobjecttestcas:9,call:[0,3,4,5,6,8],callabl:8,callback:[3,6,8],callback_url:8,callbackhandl:8,can:[0,2,3,5,6,8,10,12],cannot:[6,12],categori:3,certain:6,check:[3,5],check_non:3,checkin:3,checkintyp:3,choic:[],circumv:3,citi:2,client:[3,5,6,8],clientsid:[3,5,8],clone:[],close_connect:5,coarsen:[0,2],code:[0,2,3,12],collect:[0,2,3,5,12],column:6,combin:[2,12],comma:6,command:11,comment:[2,3,6],commit:6,common:[0,2,4],commonli:3,commun:0,complement:7,complet:[3,6,8],complete_authent:[3,8],completeconsenthandl:8,complex:8,compon:[2,3,13],concept:[],concern:0,concret:3,condit:12,confid:8,configur:11,confirm:[3,8],conflict:11,connect:[5,8],connection_str:[5,8],consent:[0,5,6,8,12],consent_confirm:8,consentflowhandl:8,consider:0,consist:[0,2,3,5,12],constraint:12,construct:[2,3,8],consum:[2,3],consumpt:8,contact:8,contain:[0,2,3,7,8,11,12],content:1,context:[2,6,8],continu:[3,5,8],contribut:0,convent:[3,7],convert:[2,3,8],cooki:[6,8],coordin:[2,8],core:3,correct:[2,8],correctli:[9,11],correspond:[3,5,6,8],count:3,counterpart:[2,8],countri:2,coupl:12,cover:3,coverag:0,coverphoto:3,crawl:0,crawler:0,creat:[2,3,4,6,8],create_app:6,create_user_all_permiss:4,create_user_no_permiss:4,creation:[0,2],credenti:5,criteria:[3,6,8],current:[],data:[0,2,3,4,5,6,8,12],databas:[0,5,6,8],date:3,datetimejsonhandl:2,db_string:8,deal:3,debug:3,declar:0,decor:8,def:3,degrad:0,deleg:9,delet:[3,4],delight:0,demonstr:[3,12],depend:[2,3,8,11],deploi:0,descript:2,design:[0,2,3,5,6,8,12],destroi:8,destruct:2,determin:3,develop:[],dict:[3,4,5,8],dictionari:[2,3,4,5,8],differ:8,difficult:2,direct:0,directli:[3,5,8],directori:[7,11],disallowedbyprivacypolicyerror:8,dispatch_request:6,displai:[11,12],displaynam:2,distinct:8,distribut:0,do_build_schema:5,docker:[],doe:[3,8],doesn:8,don:7,done:[3,8],drop_first:5,durat:8,dure:[2,6,8,12],each:[2,3,6,7,8],earth:2,easiest:11,easili:12,educ:3,effect:12,either:3,element:12,elementtre:[5,8],elsewher:3,email:[3,8],emb:2,embed:3,empti:6,enabl:4,encod:[2,6,12],end:[2,6],endpoint:[3,4],endtim:2,enforc:12,engag:12,engin:0,ensur:[0,5,8,9],entir:[3,8],entiti:3,entrypoint:8,environ:[6,11,12],error:[6,8],escap:6,essenti:3,etc:[2,3,7,8],ethic:[0,12],evalu:[6,8],even:[2,12],event:[2,6],everi:[2,4],everyth:11,everywher:3,exampl:[2,3,6,8,12],except:1,exchang:[2,3],execut:0,exist:[3,8],exp_design:[5,8],expect:[2,3,6,8,9],experi:[5,6,11],experiment:[0,3,5,6,8,12],experimental_design:[5,8],experimentbuild:[1,5],experimentnt:6,explicitli:3,expos:[2,3,6,8],express:[0,6,8],extend:3,extern:[2,3,8],extract:3,facebook:[0,3,12],facebook_obj:3,facebookgatewai:1,facebookgatewaytest:[],facebookservicegatewai:3,factor:8,fail:8,fals:[3,5,8],familiar:[0,11],favourit:6,field:[3,8],file:[8,12],film:3,filter:[6,8],find_nth:6,first:11,firstnam:3,fit:[7,8],flatten:2,flexibl:2,flow:[3,5,6,8,9],follow:[0,2,3,6,8,10,11,12,13],footprint:6,forc:3,form:[0,2,3,6,8,12],format:[2,3],found:[5,8],framework:0,free:2,friend:3,friendli:[2,8],friendlier:[5,8],from:[5,6],full:[0,2,3,6,8,12],fullimag:2,fundament:8,further:6,futur:[0,3,6],g43519500:6,gatewai:1,gatewaynam:3,gender:3,gener:[0,2,3,5,8,12],generate_permissions_list:3,geo:3,geograph:2,get:[5,6],get_bad_processor:[4,9],get_builder_refer:6,get_com:3,get_disallow_processor:9,get_empty_processor:4,get_existing_provider_auth:5,get_friendly_nam:[2,3],get_good_processor:[4,9],get_good_prop:4,get_graph_data:3,get_lik:3,get_particip:[5,8],get_prop:[5,8],get_service_gatewai:8,get_tabl:5,get_valu:3,getobject:[3,8],getobject_returns_object:9,getobjectjson:8,getobjectjsontestcas:9,getpermissionsforpolicytestcas:4,github:[],given:[3,4,5,6,8,12],good:6,gracefulli:[0,6],graph:[3,4],graphic:2,great:3,guarante:[0,3,6],guid:11,handl:[0,3,4,6,8,12],handler:2,handshak:6,have:[0,2,3,6,11,12],haystack:[3,6],head:11,header:[3,6],height:3,held:3,help:[0,10,11],here:3,histori:3,hometown:3,hope:3,host:8,hous:2,how:[0,3,6,8,12,13],howev:[3,8],http:3,httprequest:3,hub:11,human:[2,8,12],ideal:[2,12],identifi:[0,2,3,6,8],imag:[2,3,11],imagetestcas:4,immedi:6,implement:[2,3,8],implic:[],improv:[0,3],inaccess:2,inadvert:12,includ:[0,2,5,6,8,11,12],incorrectli:8,incorrectsecreterror:8,indefinit:3,index:0,individu:0,inferattributestestcas:9,inferobjecttestcas:9,inform:[0,3,6,8,11,12],ingest:0,inherit:3,init:4,initi:[2,3,6],initialisetestcas:4,inject:[3,8],innard:8,inreplyto:[2,3,6],insert:[5,6],instal:[],instanc:[0,2,3,6,8,11],instanti:[5,8],instead:[5,6],instig:[3,8],intend:[0,2,3,6],interact:[3,8],interest:0,interestedin:3,interfac:[0,3,5,6,8],intern:[2,3,4,5,6,8],interpet:5,interpret:6,interrog:3,interv:2,intervent:[0,5],introduc:[3,13],invalid:[6,8],invalidpolicyprovidederror:8,invalidprivacypolici:8,invalidtransformationlevelerror:2,invok:[0,8],involv:[2,8],ioerror:[5,8],irb:12,irrecover:6,iso:[2,3],isol:11,isreadi:6,issu:0,iter:[11,12],json:[3,5,6,8],json_obj:3,jsonpickl:2,just:3,kei:6,keywarg:9,kind:[0,13],know:8,kwarg:8,label:2,lambda:[6,8],languag:[2,3],larger:6,last:[0,2,3,6,8],lastfm:[6,8],lastfmgatewai:1,lastfmgatewaytest:[],lastfmservicegatewai:3,lastnam:3,lat:2,later:6,latest:11,latitud:2,layer:6,let:[3,8],level:[2,3],librari:[],life:2,lifecycl:8,lightweight:[3,6],like:[0,3],limit:3,line:11,link:[2,3],list:[2,3,6,8],liter:8,literatur:3,live:7,lng:2,load:3,local:[],localhost:11,locat:[2,3],logic:[2,7,8],longer:0,longev:0,longitud:2,look:3,lookup:6,love:3,lukeweb:8,machin:11,made:[3,8],mai:[2,3,6,8,11],mail:2,main:2,mainli:3,maintain:[0,3,8],make:[2,3,5,6,8,11],manag:[5,6,8],mandatori:3,mani:8,map:[0,2,3,11],mapped_port:11,markup:2,match:[3,6],maximum:2,maybeattend:2,mean:3,meaning:8,mechan:[3,8],memori:6,messag:[2,11],meta_t:5,metadata:[0,3,5],method:[3,8],methodnam:[4,7,9],microblog:2,middl:3,middlenam:3,might:[2,8],miss:8,mobil:3,modifi:3,modul:1,more:[8,11,12],most:[2,3],movi:3,much:7,multi:6,multipl:[],music:3,must:[2,3,4,5,6,8],name:[2,3,5,8],namespac:8,nativ:8,natur:[2,12],necessari:[3,8],need:[0,3,8,12],needl:[3,6],nest:8,network:[0,3,12],newer:0,next:11,non:2,none:[3,5,6,8],noprivacypolicyprovidederror:8,notattend:2,note:[2,3,6,8],now:[11,12],number:[2,3],obj:2,object:[2,3,4,5,6,8,9],object_id:3,object_nam:6,object_to_cach:8,object_typ:[3,8],objecttyp:3,occur:2,off:[],offlin:12,offset:3,often:2,old:3,older:0,on_begin:6,on_cancel:6,on_complet:6,on_confirm:6,on_cons:6,on_fallback:6,on_get_object:6,on_handshak:6,on_invalid:6,on_post_respons:6,on_publish_object:6,on_regist:6,on_schema:6,on_session_read:6,on_session_timeout:6,on_session_writ:6,onc:[3,8],onli:[0,3,6,8,12],onlin:2,onward:6,openli:11,oper:[3,8],operationnotimplementederror:8,option:[3,8],order:3,orient:3,origin:[3,5,6,8],other:[0,3,8,10,12,13],otherwis:[3,5],our:[6,11],outgo:8,outlin:12,own:[2,3,6,7,8],pack:2,packag:1,page:[0,3],param:[3,4,5,8],paramet:[2,3,4,5,6,8],pars:[3,5,8],parse_com:3,parse_json:3,parse_lik:3,parse_loc:3,parse_tag:3,part:3,parti:8,particip:[0,3,5,6,8,12],participant_id:[5,8],particularli:8,pass:[3,6,8],path:[3,4,5,8],pattern:6,payload:[3,6,8],peopl:[2,3],per:8,perform:[3,4,6,8],period:6,permalink:[2,3],permament:2,perman:[2,6],permiss:[3,4],persist:1,persistencemanag:1,person:[2,3,8],perspect:12,photo:[2,3,8],physic:2,pictur:3,pip:11,pipe:8,pixel:3,pixi:6,place:[2,3,8,12],plain:[2,8],platform:12,playlist:3,pleas:0,point:[2,6],polici:[5,6],policy_processor:5,policydocumentgener:1,policyprocessor:1,policyprocessortest:[],polit:3,politicalview:3,popul:3,port:11,posit:[2,3],position_as_dict:2,possibl:[2,3,5],post:[2,3,4,6,8],post_graph_data:[3,4],post_respons:[5,8],post_response_json:5,postal:2,postalcod:2,postobject:8,postobjectjson:8,potenti:3,practic:12,pre:[8,11],prefer:3,prefix:8,prepar:11,prerequisit:[],present:8,previou:[3,6],previous:[3,5],primari:6,print:2,prisess:6,prisoner_id:[5,6,8],privaci:[5,6],privacy_polici:8,probabl:[0,11],problem:0,proce:8,process:[3,8],processor:8,processorinferobject_returns_person:9,profil:[3,6,12],progress:0,prop:[3,4,5],properti:2,protocol:12,provid:[2,3,5,6,8],provide_contact:8,provide_db_str:8,provide_experimental_design:8,provide_privacy_polici:8,provide_titl:8,providepoliciestestcas:9,providerauthenthandl:8,publish:[0,2,3,4,6,8,12],pull:[0,11],push:[8,11],put:8,pylast:3,python:[8,11,12],queri:[3,4,6,8],question:[6,12],quickest:[],quickli:11,rais:[0,2,5,8],rang:[2,3],rather:[8,11],read:[3,6,8,13],readabl:[2,6,8,12],readi:[0,6],reauthent:5,rebuild_engin:5,receiv:[3,5,6,8],recommend:[10,11,13],recov:6,redirect:[3,8],reduc:2,refer:[0,5,8],reflect:12,refresh:3,region:2,regist:[3,5,6,8,12],register_particip:[5,8],register_participant_with_provid:5,relat:[2,3,6,8],relationship:3,relationshipstatu:3,releas:[0,11],relev:[2,4,5,8],religion:3,remov:6,render:8,render_templ:6,replac:3,repli:[2,3],replic:12,repositori:11,repres:[2,3],represent:[2,3,8,12],reproduc:[0,10,12],request:[0,3,5,6,8,9],request_authent:[3,8],request_handl:3,requesthandl:8,requir:[0,3,5,6,8,11,12],requst_authent:8,research:[0,8,12],resolv:11,resourc:[2,3],respond:2,respons:[0,2,3,5,6,8],rest:[3,6,8],restart:6,restor:[2,3],restore_authent:[3,8],result:[3,6],retain:6,retreiv:3,retriev:[2,3,5,6,8,12],review:[8,12],rich:2,row:5,rsvp:2,rule:[0,12],run:[0,4,7,8,11,12],runner:7,runtest:[4,7,9],runtim:12,runtimeprivacypolicyparsererror:8,safe:6,sai:2,said:3,same:[3,6,8,12],sanitis:[0,2,3,5,8,12],sanitiseobjectrequesttestcas:9,sarhead:3,satisfi:0,scema:5,schema:[5,6,8],scheme:3,scope:8,scrape:0,search:0,second:[3,8],secret:8,see:[3,7,8,11],segreg:7,self:[2,3],semant:[2,8],sens:2,sensit:[0,8],sentenc:[2,8],seper:6,serial:2,server:[1,5],server_url:8,servic:[0,2,3,5,6,7,8,9,12],servicegatewai:1,servicegatewaynotfound:8,servicegatewaynotfounderror:8,session:[3,5,6,8],set:[2,3,4,6,11,12],set_builder_refer:6,set_test_user_attribut:4,setup:[4,7,9],sever:2,sexual:3,sha224:2,share:[2,12],shorter:2,should:[2,3,5,6,8,11],shout:3,show:12,side:[3,5],signal:5,signatur:3,signific:3,significantoth:3,similar:[3,8],similarli:8,simpl:[0,6,10,12],simpli:3,simplic:[],simplifi:0,singl:[0,8],site:[0,3,12],size:[2,3],small:2,social:[0,2,3,5,6,8,12],social_object:3,socialactivityrespons:3,socialgatewaytest:[],socialobject:1,socialobjectgatewai:1,socialobjectgatewaytest:[],socialobjectnotsupportederror:8,socialobjectsgatewai:[5,8],socialobjectstestcas:7,sog:[5,8],some:[4,8,12],someon:[3,8],somewher:3,speak:3,spec:8,specialis:[2,3],specif:3,specifi:[3,8],spin:[],sqlalchemi:0,stabil:11,stage:[3,8],standard:[2,3,12],standardis:12,start:[],start_respons:6,starttim:2,state:[2,6,8],statu:[2,3],status:3,statuslist:3,statustestcas:4,steer:0,step:[6,8],still:3,storag:5,store:[0,3,5,6,8,12],str:[2,3,4,5,8],str_to_tim:3,strategi:12,street:2,streetaddress:2,string:[2,3,6,8],strongli:[10,11],stub:3,studi:[0,12],subclass:[2,3],subject:[5,8],submodul:1,subpackag:1,subsequ:[6,8],subset:8,succes:3,success:[3,8],successfulli:5,suggest:0,suit:[7,9],suitabl:3,summari:12,superclass:3,suppli:[3,8],support:[0,2,3,12,13],sure:11,surfac:3,syntax:[0,8],system:[0,11],table_nam:5,table_typ:5,tag:[2,3,8,11],take:[3,8],target:[],tast:3,template_nam:6,temporari:[6,8],temporarili:6,term:2,test:1,test_bad_attribut:9,test_bad_format:9,test_bad_get:9,test_bad_nested_obj:9,test_bad_obj:9,test_bad_polici:[4,9],test_bad_prop:4,test_bad_request_badobject:9,test_bad_request_badoper:9,test_bad_token:4,test_cache_hit:9,test_cache_miss:9,test_fail_valid:9,test_get_failur:4,test_get_success:4,test_good_get:[4,9],test_good_liter:9,test_good_nested_obj:9,test_good_obj:9,test_good_polici:[4,9],test_good_prop:4,test_good_respons:9,test_good_token:4,test_good_valid:9,test_invalid_bas:9,test_invalid_liter:9,test_invalid_social_gatewai:9,test_logic_failonand:9,test_logic_failonimplicitand:9,test_logic_failonnest:9,test_logic_failonor:9,test_malformed_head:9,test_malformed_respons:9,test_missing_bas:9,test_missing_head:9,test_no_allow_attribut:9,test_no_polici:[4,9],test_no_prop:4,test_no_token:4,test_post:4,test_provide_good_exp_design:9,test_provide_good_privacy_polici:9,test_provide_invalid_exp_design:9,test_provide_invalid_privacy_polici:9,test_valid_bas:9,test_valid_social_gatewai:9,testcas:[4,7,9],text:[2,8],textual:[2,3],than:[2,8,11,12],thei:[0,2,3,7,8,12],them:[0,3,5,8],themselv:[3,8],thi:[5,6,9,11],threaded_get_object:6,three:12,through:[3,5,6,8],throughout:[3,8],thu:3,thumb:0,thumbnail:3,time:[2,3],timelin:3,timezon:3,titl:[3,8],todo:11,token:[3,4,5,6,8],too:7,tool:0,tornado:8,town:2,track:[0,3,6],trade:[],transform:[2,3],transform_artist:3,transform_hash:2,transform_reduc:2,transpar:3,trivial:0,tupl:5,turn:8,tutori:[],tweet:[3,12],twitter:[0,3],twittergatewai:1,twitterservicegatewai:3,two:[3,8,10,11],txt:11,type:[2,3,5,6,8,12],typic:3,uid:3,under:[0,12],underli:[11,12],understand:[2,8,13],unescap:8,uniqu:[2,3,8],unit:7,unittest:[4,7,9],unnecessari:[],until:12,updat:[2,3,4],updatedtim:3,upload:[2,3],uri:[2,3],url:[2,3,6,8],usabl:8,user:[0,3,4,6,8,12],usernam:3,usertestcas:4,usual:[3,6,8],utc:3,util:0,valid:[3,5,6,8],validate_design:5,validate_polici:8,validateobjectrequesttestcas:9,validatepolicytestcas:9,valu:[2,3,4,6,8],verifi:8,version:[0,2,3,6,8],via:[0,3,11],video:2,villag:2,violat:12,virtual:11,virtualenv:11,visit:[3,6,8,11],visual:2,wai:[3,8,11],wall:3,want:[6,11],web:[5,6,8,12],webservic:1,well:[3,8],were:3,werkzeug:8,whatev:8,when:[2,3,6,8],where:[0,2,3,5,6,7,8,11],wherea:8,whether:[3,5],which:[0,2,3,6,8,11,12],who:[2,3,4],who_for:8,whose:[3,6],width:3,wildcard:6,within:[3,11],without:[2,6,8,11],word:2,work:[3,11,13],workflow:1,worri:[7,11],would:0,wrap:[0,3],wrapped_head:3,wrappedrespons:3,wrapper:[3,5,8],write:[5,6,11],written:12,wrote:2,wsgi:11,wsgi_app:6,xml:[5,8,12],yet:[0,6],yield:12,you:[0,3,6,7,8,10,11,12],your:[6,7,11],yourself:8,yyyi:3,zip:2},titles:["PRISONER","&lt;no title&gt;","prisoner package","prisoner.gateway package","prisoner.gateway.tests package","prisoner.persistence package","prisoner.server package","prisoner.tests package","prisoner.workflow package","prisoner.workflow.tests package","Tutorials","Installing PRISONER","Writing your first experiment","Key concepts"],titleterms:{clone:11,concept:13,content:[2,3,4,5,6,7,8,9],current:0,develop:[0,11],docker:11,document:[],except:8,experi:12,experimentbuild:8,facebookgatewai:3,facebookgatewaytest:4,featur:0,first:12,from:11,gatewai:[3,4],get:[],github:11,indic:0,instal:11,kei:13,lastfmgatewai:3,lastfmgatewaytest:4,local:11,modul:[2,3,4,5,6,7,8,9],packag:[2,3,4,5,6,7,8,9],persist:5,persistencemanag:5,polici:12,policydocumentgener:8,policyprocessor:8,policyprocessortest:9,prerequisit:12,prison:[0,2,3,4,5,6,7,8,9,11],privaci:12,quickest:[],server:6,servicegatewai:3,socialgatewaytest:4,socialobject:2,socialobjectgatewai:8,socialobjectgatewaytest:9,spin:11,start:[],submodul:[2,3,4,5,6,7,8,9],subpackag:[2,3,8],tabl:0,test:[4,7,9],thi:12,tutori:[10,12],twittergatewai:3,webservic:6,welcom:[],what:0,workflow:[8,9],write:12,your:12}})