//Maya ASCII 2013 scene
//Name: lipsBase.ma
//Last modified: Fri, Nov 29, 2013 03:37:56 PM
//Codeset: 1252
requires maya "2013";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2013";
fileInfo "version" "2013 x64";
fileInfo "cutIdentifier" "201202220241-825136";
fileInfo "osv" "Microsoft Windows 7 Ultimate Edition, 64-bit Windows 7 Service Pack 1 (Build 7601)\n";
createNode transform -n "mouth_base_control_grp";
	setAttr ".rp" -type "double3" -0.00019086096813603071 102.65491598430607 10.647468623764977 ;
	setAttr ".sp" -type "double3" -0.00019086096813603071 102.65491598430607 10.647468623764977 ;
createNode transform -n "points_base_mouth_grp" -p "mouth_base_control_grp";
createNode transform -n "mouth_point_0_loc" -p "points_base_mouth_grp";
	setAttr ".rp" -type "double3" 1.871 102.57085829900721 10.137053342026432 ;
	setAttr ".sp" -type "double3" 1.871 102.57085829900721 10.137053342026432 ;
createNode locator -n "mouth_point_0_locShape" -p "mouth_point_0_loc";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" 1.871 102.57085829900721 10.137053342026432 ;
	setAttr ".los" -type "double3" -0.20000000000000018 -0.20000000000000018 -0.20000000000000018 ;
createNode transform -n "cluster9Handle" -p "mouth_point_0_loc";
	setAttr -l on ".v" no;
	setAttr ".rp" -type "double3" 1.871 102.57085829900721 10.137053342026432 ;
	setAttr ".sp" -type "double3" 1.871 102.57085829900721 10.137053342026432 ;
createNode clusterHandle -n "cluster9HandleShape" -p "cluster9Handle";
	setAttr ".ihi" 0;
	setAttr -k off ".v";
	setAttr ".or" -type "double3" 1.871 102.57085829900721 10.137053342026432 ;
createNode transform -n "mouth_point_1_loc" -p "points_base_mouth_grp";
	setAttr ".rp" -type "double3" 1.058 102.84263221335118 10.754520798307015 ;
	setAttr ".sp" -type "double3" 1.058 102.84263221335118 10.754520798307015 ;
createNode locator -n "mouth_point_1_locShape" -p "mouth_point_1_loc";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" 1.058 102.84263221335118 10.754520798307015 ;
	setAttr ".los" -type "double3" -0.20000000000000018 -0.20000000000000018 -0.20000000000000018 ;
createNode transform -n "cluster4Handle" -p "mouth_point_1_loc";
	setAttr -l on ".v" no;
	setAttr ".rp" -type "double3" 1.058 102.84263221335118 10.754520798307015 ;
	setAttr ".sp" -type "double3" 1.058 102.84263221335118 10.754520798307015 ;
createNode clusterHandle -n "cluster4HandleShape" -p "cluster4Handle";
	setAttr ".ihi" 0;
	setAttr -k off ".v";
	setAttr ".or" -type "double3" 1.058 102.84263221335118 10.754520798307015 ;
createNode transform -n "mouth_point_2_loc" -p "points_base_mouth_grp";
	setAttr ".rp" -type "double3" 0 102.87309065865472 11.157883905503523 ;
	setAttr ".sp" -type "double3" 0 102.87309065865472 11.157883905503523 ;
createNode locator -n "mouth_point_2_locShape" -p "mouth_point_2_loc";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" 0 102.87309065865472 11.157883905503523 ;
	setAttr ".los" -type "double3" -0.20000000000000018 -0.20000000000000018 -0.20000000000000018 ;
createNode transform -n "cluster3Handle" -p "mouth_point_2_loc";
	setAttr -l on ".v" no;
	setAttr ".rp" -type "double3" 0 102.87309065865472 11.157883905503523 ;
	setAttr ".sp" -type "double3" 0 102.87309065865472 11.157883905503523 ;
createNode clusterHandle -n "cluster3HandleShape" -p "cluster3Handle";
	setAttr ".ihi" 0;
	setAttr -k off ".v";
	setAttr ".or" -type "double3" 0 102.87309065865472 11.157883905503523 ;
createNode transform -n "mouth_point_3_loc" -p "points_base_mouth_grp";
	setAttr ".rp" -type "double3" 1.046 102.49910822373417 10.760242877346744 ;
	setAttr ".sp" -type "double3" 1.046 102.49910822373417 10.760242877346744 ;
createNode locator -n "mouth_point_3_locShape" -p "mouth_point_3_loc";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" 1.046 102.49910822373417 10.760242877346744 ;
	setAttr ".los" -type "double3" -0.20000000000000018 -0.20000000000000018 -0.20000000000000018 ;
createNode transform -n "cluster7Handle" -p "mouth_point_3_loc";
	setAttr -l on ".v" no;
	setAttr ".rp" -type "double3" 1.046 102.49910822373417 10.760242877346744 ;
	setAttr ".sp" -type "double3" 1.046 102.49910822373417 10.760242877346744 ;
createNode clusterHandle -n "cluster7HandleShape" -p "cluster7Handle";
	setAttr ".ihi" 0;
	setAttr -k off ".v";
	setAttr ".or" -type "double3" 1.046 102.49910822373417 10.760242877346744 ;
createNode transform -n "mouth_point_4_loc" -p "points_base_mouth_grp";
	setAttr ".rp" -type "double3" 0 102.43674130995743 11.139950034852291 ;
	setAttr ".sp" -type "double3" 0 102.43674130995743 11.139950034852291 ;
createNode locator -n "mouth_point_4_locShape" -p "mouth_point_4_loc";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" 0 102.43674130995743 11.139950034852291 ;
	setAttr ".los" -type "double3" -0.20000000000000018 -0.20000000000000018 -0.20000000000000018 ;
createNode transform -n "cluster6Handle" -p "mouth_point_4_loc";
	setAttr -l on ".v" no;
	setAttr ".rp" -type "double3" 0 102.43674130995743 11.139950034852291 ;
	setAttr ".sp" -type "double3" 0 102.43674130995743 11.139950034852291 ;
createNode clusterHandle -n "cluster6HandleShape" -p "cluster6Handle";
	setAttr ".ihi" 0;
	setAttr -k off ".v";
	setAttr ".or" -type "double3" 0 102.43674130995743 11.139950034852291 ;
createNode transform -n "mouth_point_5_loc" -p "points_base_mouth_grp";
	setAttr ".rp" -type "double3" -1.8713817219362721 102.57085829900721 10.137053342026432 ;
	setAttr ".sp" -type "double3" -1.8713817219362721 102.57085829900721 10.137053342026432 ;
createNode locator -n "mouth_point_5_locShape" -p "mouth_point_5_loc";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" -1.8713817219362721 102.57085829900721 10.137053342026432 ;
	setAttr ".los" -type "double3" -0.20000000000000018 -0.20000000000000018 -0.20000000000000018 ;
createNode transform -n "cluster8Handle" -p "mouth_point_5_loc";
	setAttr -l on ".v" no;
	setAttr ".rp" -type "double3" -1.8713817219362721 102.57085829900721 10.137053342026432 ;
	setAttr ".sp" -type "double3" -1.8713817219362721 102.57085829900721 10.137053342026432 ;
createNode clusterHandle -n "cluster8HandleShape" -p "cluster8Handle";
	setAttr ".ihi" 0;
	setAttr -k off ".v";
	setAttr ".or" -type "double3" -1.8713817219362721 102.57085829900721 10.137053342026432 ;
createNode transform -n "mouth_point_6_loc" -p "points_base_mouth_grp";
	setAttr ".rp" -type "double3" -1.0583492360233946 102.84263221335118 10.754520798307015 ;
	setAttr ".sp" -type "double3" -1.0583492360233946 102.84263221335118 10.754520798307015 ;
createNode locator -n "mouth_point_6_locShape" -p "mouth_point_6_loc";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" -1.0583492360233946 102.84263221335118 10.754520798307015 ;
	setAttr ".los" -type "double3" -0.20000000000000018 -0.20000000000000018 -0.20000000000000018 ;
createNode transform -n "cluster2Handle" -p "mouth_point_6_loc";
	setAttr -l on ".v" no;
	setAttr ".rp" -type "double3" -1.0583492360233946 102.84263221335118 10.754520798307015 ;
	setAttr ".sp" -type "double3" -1.0583492360233946 102.84263221335118 10.754520798307015 ;
createNode clusterHandle -n "cluster2HandleShape" -p "cluster2Handle";
	setAttr ".ihi" 0;
	setAttr -k off ".v";
	setAttr ".or" -type "double3" -1.0583492360233946 102.84263221335118 10.754520798307015 ;
createNode transform -n "mouth_point_7_loc" -p "points_base_mouth_grp";
	setAttr ".rp" -type "double3" -1.0459557787807525 102.49910822373417 10.760242877346744 ;
	setAttr ".sp" -type "double3" -1.0459557787807525 102.49910822373417 10.760242877346744 ;
createNode locator -n "mouth_point_7_locShape" -p "mouth_point_7_loc";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" -1.0459557787807525 102.49910822373417 10.760242877346744 ;
	setAttr ".los" -type "double3" -0.20000000000000018 -0.20000000000000018 -0.20000000000000018 ;
createNode transform -n "cluster5Handle" -p "mouth_point_7_loc";
	setAttr -l on ".v" no;
	setAttr ".rp" -type "double3" -1.0459557787807525 102.49910822373417 10.760242877346744 ;
	setAttr ".sp" -type "double3" -1.0459557787807525 102.49910822373417 10.760242877346744 ;
createNode clusterHandle -n "cluster5HandleShape" -p "cluster5Handle";
	setAttr ".ihi" 0;
	setAttr -k off ".v";
	setAttr ".or" -type "double3" -1.0459557787807525 102.49910822373417 10.760242877346744 ;
createNode transform -n "bottom_base_mouth_crv" -p "mouth_base_control_grp";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr ".it" no;
createNode nurbsCurve -n "bottom_base_mouth_crvShape" -p "bottom_base_mouth_crv";
	setAttr -k off ".v";
	setAttr -s 12 ".iog[0].og";
	setAttr ".tw" yes;
createNode nurbsCurve -n "bottom_base_mouth_crvShape2Orig" -p "bottom_base_mouth_crv";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		3 2 0 no 3
		7 0 0 0 1 2 2 2
		5
		-1.8713817219362721 102.57085829900721 10.137053342026432
		-1.0459557787807525 102.49910822373417 10.760242877346744
		0 102.43674130995743 11.139950034852291
		1.046 102.49910822373417 10.760242877346744
		1.871 102.57085829900721 10.137053342026432
		;
createNode transform -n "top_base_mouth_crv" -p "mouth_base_control_grp";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr ".it" no;
createNode nurbsCurve -n "top_base_mouth_crvShape" -p "top_base_mouth_crv";
	setAttr -k off ".v";
	setAttr -s 12 ".iog[0].og";
	setAttr ".tw" yes;
createNode nurbsCurve -n "top_base_mouth_crvShape1Orig" -p "top_base_mouth_crv";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		3 2 0 no 3
		7 0 0 0 1 2 2 2
		5
		-1.8713817219362721 102.57085829900721 10.137053342026432
		-1.0583492360233946 102.84263221335118 10.754520798307015
		0 102.87309065865472 11.157883905503523
		1.0580000000000001 102.84263221335118 10.754520798307015
		1.871 102.57085829900721 10.137053342026432
		;
createNode cluster -n "cluster9";
	setAttr -s 2 ".ip";
	setAttr -s 2 ".og";
	setAttr -s 2 ".gm";
	setAttr ".gm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".gm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode objectSet -n "cluster9Set";
	setAttr ".ihi" 0;
	setAttr -s 2 ".dsm";
	setAttr ".vo" yes;
	setAttr -s 2 ".gn";
createNode groupId -n "cluster9GroupId";
	setAttr ".ihi" 0;
createNode groupId -n "cluster9GroupId1";
	setAttr ".ihi" 0;
createNode groupParts -n "cluster9GroupParts";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[4]";
createNode cluster -n "cluster8";
	setAttr -s 2 ".ip";
	setAttr -s 2 ".og";
	setAttr -s 2 ".gm";
	setAttr ".gm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".gm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode objectSet -n "cluster8Set";
	setAttr ".ihi" 0;
	setAttr -s 2 ".dsm";
	setAttr ".vo" yes;
	setAttr -s 2 ".gn";
createNode groupId -n "cluster8GroupId";
	setAttr ".ihi" 0;
createNode groupId -n "cluster8GroupId1";
	setAttr ".ihi" 0;
createNode groupParts -n "cluster8GroupParts";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[0]";
createNode cluster -n "cluster4";
	setAttr ".gm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode objectSet -n "cluster4Set";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "cluster4GroupId";
	setAttr ".ihi" 0;
createNode groupParts -n "cluster4GroupParts";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[3]";
createNode cluster -n "cluster3";
	setAttr ".gm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode objectSet -n "cluster3Set";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "cluster3GroupId";
	setAttr ".ihi" 0;
createNode groupParts -n "cluster3GroupParts";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[2]";
createNode cluster -n "cluster2";
	setAttr ".gm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode objectSet -n "cluster2Set";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "cluster2GroupId";
	setAttr ".ihi" 0;
createNode groupParts -n "cluster2GroupParts";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[1]";
createNode tweak -n "tweak1";
createNode objectSet -n "tweakSet1";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "groupId3";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts2";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*]";
createNode groupParts -n "cluster8GroupParts1";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[0]";
createNode cluster -n "cluster7";
	setAttr ".gm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode objectSet -n "cluster7Set";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "cluster7GroupId";
	setAttr ".ihi" 0;
createNode groupParts -n "cluster7GroupParts";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[3]";
createNode cluster -n "cluster6";
	setAttr ".gm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode objectSet -n "cluster6Set";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "cluster6GroupId";
	setAttr ".ihi" 0;
createNode groupParts -n "cluster6GroupParts";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[2]";
createNode cluster -n "cluster5";
	setAttr ".gm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode objectSet -n "cluster5Set";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "cluster5GroupId";
	setAttr ".ihi" 0;
createNode groupParts -n "cluster5GroupParts";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[1]";
createNode tweak -n "tweak2";
createNode objectSet -n "tweakSet2";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "groupId5";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts4";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*]";
createNode groupParts -n "cluster9GroupParts1";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[4]";
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :renderPartition;
	setAttr -s 3 ".st";
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultShaderList1;
	setAttr -s 3 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :renderGlobalsList1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
select -ne :defaultHardwareRenderGlobals;
	setAttr ".fn" -type "string" "im";
	setAttr ".res" -type "string" "ntsc_4d 646 485 1.333";
select -ne :ikSystem;
	setAttr -s 4 ".sol";
connectAttr "cluster9.og[1]" "bottom_base_mouth_crvShape.cr";
connectAttr "tweak2.pl[0].cp[0]" "bottom_base_mouth_crvShape.twl";
connectAttr "cluster5GroupId.id" "bottom_base_mouth_crvShape.iog.og[0].gid";
connectAttr "cluster5Set.mwc" "bottom_base_mouth_crvShape.iog.og[0].gco";
connectAttr "groupId5.id" "bottom_base_mouth_crvShape.iog.og[1].gid";
connectAttr "tweakSet2.mwc" "bottom_base_mouth_crvShape.iog.og[1].gco";
connectAttr "cluster6GroupId.id" "bottom_base_mouth_crvShape.iog.og[2].gid";
connectAttr "cluster6Set.mwc" "bottom_base_mouth_crvShape.iog.og[2].gco";
connectAttr "cluster7GroupId.id" "bottom_base_mouth_crvShape.iog.og[3].gid";
connectAttr "cluster7Set.mwc" "bottom_base_mouth_crvShape.iog.og[3].gco";
connectAttr "cluster8GroupId1.id" "bottom_base_mouth_crvShape.iog.og[5].gid";
connectAttr "cluster8Set.mwc" "bottom_base_mouth_crvShape.iog.og[5].gco";
connectAttr "cluster9GroupId1.id" "bottom_base_mouth_crvShape.iog.og[6].gid";
connectAttr "cluster9Set.mwc" "bottom_base_mouth_crvShape.iog.og[6].gco";
connectAttr "cluster9.og[0]" "top_base_mouth_crvShape.cr";
connectAttr "tweak1.pl[0].cp[0]" "top_base_mouth_crvShape.twl";
connectAttr "groupId3.id" "top_base_mouth_crvShape.iog.og[1].gid";
connectAttr "tweakSet1.mwc" "top_base_mouth_crvShape.iog.og[1].gco";
connectAttr "cluster2GroupId.id" "top_base_mouth_crvShape.iog.og[2].gid";
connectAttr "cluster2Set.mwc" "top_base_mouth_crvShape.iog.og[2].gco";
connectAttr "cluster3GroupId.id" "top_base_mouth_crvShape.iog.og[3].gid";
connectAttr "cluster3Set.mwc" "top_base_mouth_crvShape.iog.og[3].gco";
connectAttr "cluster4GroupId.id" "top_base_mouth_crvShape.iog.og[4].gid";
connectAttr "cluster4Set.mwc" "top_base_mouth_crvShape.iog.og[4].gco";
connectAttr "cluster8GroupId.id" "top_base_mouth_crvShape.iog.og[6].gid";
connectAttr "cluster8Set.mwc" "top_base_mouth_crvShape.iog.og[6].gco";
connectAttr "cluster9GroupId.id" "top_base_mouth_crvShape.iog.og[7].gid";
connectAttr "cluster9Set.mwc" "top_base_mouth_crvShape.iog.og[7].gco";
connectAttr "cluster9GroupParts.og" "cluster9.ip[0].ig";
connectAttr "cluster9GroupId.id" "cluster9.ip[0].gi";
connectAttr "cluster9GroupParts1.og" "cluster9.ip[1].ig";
connectAttr "cluster9GroupId1.id" "cluster9.ip[1].gi";
connectAttr "cluster9Handle.wm" "cluster9.ma";
connectAttr "cluster9HandleShape.x" "cluster9.x";
connectAttr "cluster9GroupId.msg" "cluster9Set.gn" -na;
connectAttr "cluster9GroupId1.msg" "cluster9Set.gn" -na;
connectAttr "top_base_mouth_crvShape.iog.og[7]" "cluster9Set.dsm" -na;
connectAttr "bottom_base_mouth_crvShape.iog.og[6]" "cluster9Set.dsm" -na;
connectAttr "cluster9.msg" "cluster9Set.ub[0]";
connectAttr "cluster8.og[0]" "cluster9GroupParts.ig";
connectAttr "cluster9GroupId.id" "cluster9GroupParts.gi";
connectAttr "cluster8GroupParts.og" "cluster8.ip[0].ig";
connectAttr "cluster8GroupId.id" "cluster8.ip[0].gi";
connectAttr "cluster8GroupParts1.og" "cluster8.ip[1].ig";
connectAttr "cluster8GroupId1.id" "cluster8.ip[1].gi";
connectAttr "cluster8Handle.wm" "cluster8.ma";
connectAttr "cluster8HandleShape.x" "cluster8.x";
connectAttr "cluster8GroupId.msg" "cluster8Set.gn" -na;
connectAttr "cluster8GroupId1.msg" "cluster8Set.gn" -na;
connectAttr "top_base_mouth_crvShape.iog.og[6]" "cluster8Set.dsm" -na;
connectAttr "bottom_base_mouth_crvShape.iog.og[5]" "cluster8Set.dsm" -na;
connectAttr "cluster8.msg" "cluster8Set.ub[0]";
connectAttr "cluster4.og[0]" "cluster8GroupParts.ig";
connectAttr "cluster8GroupId.id" "cluster8GroupParts.gi";
connectAttr "cluster4GroupParts.og" "cluster4.ip[0].ig";
connectAttr "cluster4GroupId.id" "cluster4.ip[0].gi";
connectAttr "cluster4Handle.wm" "cluster4.ma";
connectAttr "cluster4HandleShape.x" "cluster4.x";
connectAttr "cluster4GroupId.msg" "cluster4Set.gn" -na;
connectAttr "top_base_mouth_crvShape.iog.og[4]" "cluster4Set.dsm" -na;
connectAttr "cluster4.msg" "cluster4Set.ub[0]";
connectAttr "cluster3.og[0]" "cluster4GroupParts.ig";
connectAttr "cluster4GroupId.id" "cluster4GroupParts.gi";
connectAttr "cluster3GroupParts.og" "cluster3.ip[0].ig";
connectAttr "cluster3GroupId.id" "cluster3.ip[0].gi";
connectAttr "cluster3Handle.wm" "cluster3.ma";
connectAttr "cluster3HandleShape.x" "cluster3.x";
connectAttr "cluster3GroupId.msg" "cluster3Set.gn" -na;
connectAttr "top_base_mouth_crvShape.iog.og[3]" "cluster3Set.dsm" -na;
connectAttr "cluster3.msg" "cluster3Set.ub[0]";
connectAttr "cluster2.og[0]" "cluster3GroupParts.ig";
connectAttr "cluster3GroupId.id" "cluster3GroupParts.gi";
connectAttr "cluster2GroupParts.og" "cluster2.ip[0].ig";
connectAttr "cluster2GroupId.id" "cluster2.ip[0].gi";
connectAttr "cluster2Handle.wm" "cluster2.ma";
connectAttr "cluster2HandleShape.x" "cluster2.x";
connectAttr "cluster2GroupId.msg" "cluster2Set.gn" -na;
connectAttr "top_base_mouth_crvShape.iog.og[2]" "cluster2Set.dsm" -na;
connectAttr "cluster2.msg" "cluster2Set.ub[0]";
connectAttr "tweak1.og[0]" "cluster2GroupParts.ig";
connectAttr "cluster2GroupId.id" "cluster2GroupParts.gi";
connectAttr "groupParts2.og" "tweak1.ip[0].ig";
connectAttr "groupId3.id" "tweak1.ip[0].gi";
connectAttr "groupId3.msg" "tweakSet1.gn" -na;
connectAttr "top_base_mouth_crvShape.iog.og[1]" "tweakSet1.dsm" -na;
connectAttr "tweak1.msg" "tweakSet1.ub[0]";
connectAttr "top_base_mouth_crvShape1Orig.ws" "groupParts2.ig";
connectAttr "groupId3.id" "groupParts2.gi";
connectAttr "cluster7.og[0]" "cluster8GroupParts1.ig";
connectAttr "cluster8GroupId1.id" "cluster8GroupParts1.gi";
connectAttr "cluster7GroupParts.og" "cluster7.ip[0].ig";
connectAttr "cluster7GroupId.id" "cluster7.ip[0].gi";
connectAttr "cluster7Handle.wm" "cluster7.ma";
connectAttr "cluster7HandleShape.x" "cluster7.x";
connectAttr "cluster7GroupId.msg" "cluster7Set.gn" -na;
connectAttr "bottom_base_mouth_crvShape.iog.og[3]" "cluster7Set.dsm" -na;
connectAttr "cluster7.msg" "cluster7Set.ub[0]";
connectAttr "cluster6.og[0]" "cluster7GroupParts.ig";
connectAttr "cluster7GroupId.id" "cluster7GroupParts.gi";
connectAttr "cluster6GroupParts.og" "cluster6.ip[0].ig";
connectAttr "cluster6GroupId.id" "cluster6.ip[0].gi";
connectAttr "cluster6Handle.wm" "cluster6.ma";
connectAttr "cluster6HandleShape.x" "cluster6.x";
connectAttr "cluster6GroupId.msg" "cluster6Set.gn" -na;
connectAttr "bottom_base_mouth_crvShape.iog.og[2]" "cluster6Set.dsm" -na;
connectAttr "cluster6.msg" "cluster6Set.ub[0]";
connectAttr "cluster5.og[0]" "cluster6GroupParts.ig";
connectAttr "cluster6GroupId.id" "cluster6GroupParts.gi";
connectAttr "cluster5GroupParts.og" "cluster5.ip[0].ig";
connectAttr "cluster5GroupId.id" "cluster5.ip[0].gi";
connectAttr "cluster5Handle.wm" "cluster5.ma";
connectAttr "cluster5HandleShape.x" "cluster5.x";
connectAttr "cluster5GroupId.msg" "cluster5Set.gn" -na;
connectAttr "bottom_base_mouth_crvShape.iog.og[0]" "cluster5Set.dsm" -na;
connectAttr "cluster5.msg" "cluster5Set.ub[0]";
connectAttr "tweak2.og[0]" "cluster5GroupParts.ig";
connectAttr "cluster5GroupId.id" "cluster5GroupParts.gi";
connectAttr "groupParts4.og" "tweak2.ip[0].ig";
connectAttr "groupId5.id" "tweak2.ip[0].gi";
connectAttr "groupId5.msg" "tweakSet2.gn" -na;
connectAttr "bottom_base_mouth_crvShape.iog.og[1]" "tweakSet2.dsm" -na;
connectAttr "tweak2.msg" "tweakSet2.ub[0]";
connectAttr "bottom_base_mouth_crvShape2Orig.ws" "groupParts4.ig";
connectAttr "groupId5.id" "groupParts4.gi";
connectAttr "cluster8.og[1]" "cluster9GroupParts1.ig";
connectAttr "cluster9GroupId1.id" "cluster9GroupParts1.gi";
// End of lipsBase.ma
