//-
// ==========================================================================
// Copyright 1995,2006,2008 Autodesk, Inc. All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk
// license agreement provided at the time of installation or download,
// or which otherwise accompanies this software in either electronic
// or hard copy form.
// ==========================================================================
//+

#include "meshOpFty.h"

meshOpFty::meshOpFty()
//
//	Description:
//		meshOpFty constructor
//
{
	fComponentIDs.clear();
}

meshOpFty::~meshOpFty()
//
//	Description:
//		meshOpFty destructor
//
{}

void meshOpFty::setMesh( MObject& mesh )
//
//	Description:
//		Sets the mesh object for the factory to operate on
//
{
	fMesh = mesh;
}

void meshOpFty::setComponentList( MObject& componentList )
//
//	Description:
//		Sets the list of the components for the factory to operate on
//
{
	fComponentList = componentList;
}


void meshOpFty::setComponentIDs( MIntArray& componentIDs )
//
//	Description:
//		Sets the list of the components for the factory to operate on
//
{
	fComponentIDs = componentIDs;
}

void meshOpFty::setMeshOperation( MeshOperation operationType )
//
//	Description:
//		Sets the mesh operation for the factory to execute
//
{
	fOperationType = operationType;
}

void meshOpFty::setHoleData(float radius, float distance, bool outerRing, float outerRingValue,int outRingsCount, bool createHole, float innerRadius, bool additionalEdges, int innerRingsCount, int extrudeRingsCount, float rotationAngle,float flatCap )
{
	fRadius = radius;
	fDistance = distance;
	bOuterRing = outerRing;
	fOuterRingValue = outerRingValue;
	iOutRingsCount  = outRingsCount;
	bCreateHole = createHole;
	fInnerRadius = innerRadius;
	bAdditionalEdges = additionalEdges;
	iInnerRingsCount = innerRingsCount;
	iExtrudeRingsCount = extrudeRingsCount;
	fRotationAngle  = rotationAngle;
	fFlatCap = flatCap;
}


MFn::Type meshOpFty::getExpectedComponentType( MeshOperation operationType )
{
	switch (operationType)
	{
	case kSubdivideEdges: return MFn::kMeshEdgeComponent;
	case kSubdivideFaces: return MFn::kMeshPolygonComponent;
	case kExtrudeEdges: return MFn::kMeshEdgeComponent;
	case kExtrudeFaces: return MFn::kMeshPolygonComponent;
	case kCollapseEdges: return MFn::kMeshEdgeComponent;
	case kCollapseFaces: return MFn::kMeshPolygonComponent;
	case kDuplicateFaces: return MFn::kMeshPolygonComponent;
	case kExtractFaces: return MFn::kMeshPolygonComponent;
	case kSplitLightning: return MFn::kMeshPolygonComponent;
	case kChamferVertex: return MFn::kMeshVertComponent;

	default: return MFn::kInvalid;
	}
}
