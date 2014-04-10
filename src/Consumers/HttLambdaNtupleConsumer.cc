
#include <boost/algorithm/string/predicate.hpp>

#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/HttLambdaNtupleConsumer.h"


void HttLambdaNtupleConsumer::Init(Pipeline<HttTypes> * pset)
{
	// loop over all quantities containing "weight" (case-insensitive)
	// and try to find them in the weights map to write them out
	for(auto const & quantity : pset->GetSettings().GetQuantities()) {
		if(boost::algorithm::icontains(quantity, "weight")) {
			m_valueExtractorMap[quantity] = [&quantity](HttEvent const& event, HttProduct const& product) {
				return Utility::GetWithDefault(product.m_weights, quantity, 1.0);
			};
		}
	}
	m_valueExtractorMap["TauSpinnerWeight"] = [](HttEvent const & event, HttProduct const & product){
	if(product.m_weights.at("tauspinnerweight") == product.m_weights.at("tauspinnerweight")) // Avoiding 'nan' 
		return product.m_weights.at("tauspinnerweight");
	else
	{
	// 'Nan' Debug output
	LOG(DEBUG) << "\nHiggsPx=" << product.m_genBoson[0].node->p4.Px() << "|"
	<< "HiggsPy=" << product.m_genBoson[0].node->p4.Py() << "|"
	<< "HiggsPz=" << product.m_genBoson[0].node->p4.Pz() << "|"
	<< "HiggsE=" << product.m_genBoson[0].node->p4.e() << "|"
	<< "HiggsPdgId=" << product.m_genBoson[0].node->pdgId() << "|"

	<< "1TauPx=" << product.m_genBoson[0].Daughters[0].node->p4.Px() << "|"
	<< "1TauPy=" << product.m_genBoson[0].Daughters[0].node->p4.Py() << "|"
	<< "1TauPz=" << product.m_genBoson[0].Daughters[0].node->p4.Pz() << "|"
	<< "1TauE=" << product.m_genBoson[0].Daughters[0].node->p4.e() << "|"
	<< "1TauPdgId=" << product.m_genBoson[0].Daughters[0].node->pdgId() << "|"

	<< "2TauPx=" << product.m_genBoson[0].Daughters[1].node->p4.Px() << "|"
	<< "2TauPy=" << product.m_genBoson[0].Daughters[1].node->p4.Py() << "|"
	<< "2TauPz=" << product.m_genBoson[0].Daughters[1].node->p4.Pz() << "|"
	<< "2TauE=" << product.m_genBoson[0].Daughters[1].node->p4.e() << "|"
	<< "2TauPdgId=" << product.m_genBoson[0].Daughters[1].node->pdgId() << "|";

		for(unsigned int i=0; i<product.m_genBoson[0].Daughters[0].Daughters.size(); i++)
		{
			std::ostringstream index;
			index << i+1;
			//std::string Index(index.str());
			std::string name = "1Tau" + index.str() + "Daughter";
			LOG(DEBUG) << name << "Px=" << product.m_genBoson[0].Daughters[0].Daughters[i].node->p4.Px() << "|"
			<< name << "Py=" << product.m_genBoson[0].Daughters[0].Daughters[i].node->p4.Py() << "|"
			<< name << "Pz=" << product.m_genBoson[0].Daughters[0].Daughters[i].node->p4.Pz() << "|"
			<< name << "E="  << product.m_genBoson[0].Daughters[0].Daughters[i].node->p4.e() << "|"
			<< name << "PdgId=" << product.m_genBoson[0].Daughters[0].Daughters[i].node->pdgId() << "|";				
		}  

		for(unsigned int i=0; i<product.m_genBoson[0].Daughters[1].Daughters.size(); i++)
		{
			std::ostringstream index;
			index << i+1;
			//std::string Index(index.str());
			std::string name = "2Tau" + index.str() + "Daughter";
			LOG(DEBUG) << name << "Px=" << product.m_genBoson[0].Daughters[1].Daughters[i].node->p4.Px() << "|"
			<< name << "Py=" << product.m_genBoson[0].Daughters[1].Daughters[i].node->p4.Py() << "|"
			<< name << "Pz=" << product.m_genBoson[0].Daughters[1].Daughters[i].node->p4.Pz() << "|"
			<< name << "E="  << product.m_genBoson[0].Daughters[1].Daughters[i].node->p4.e() << "|"
			<< name << "PdgId=" << product.m_genBoson[0].Daughters[1].Daughters[i].node->pdgId() << "|";		
		}		
	return -777.0;
	}
 };	
	m_valueExtractorMap["PhiStar"] = [](HttEvent const & event, HttProduct const & product) {return product.m_PhiStar; };
	m_valueExtractorMap["PsiStarCP"] = [](HttEvent const & event, HttProduct const & product) {return product.m_PsiStarCP; };	
	m_valueExtractorMap["MassRoundOff1"] = [](HttEvent const & event, HttProduct const & product) {return product.m_MassRoundOff1; };
	m_valueExtractorMap["MassRoundOff2"] = [](HttEvent const & event, HttProduct const & product) {return product.m_MassRoundOff2; };
	m_valueExtractorMap["Phi"] = [](HttEvent const & event, HttProduct const & product) {return product.m_Phi; };
	//Boson
	m_valueExtractorMap["genBosonSize"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson.size(): UNDEFINED_VALUE;
	};	
	m_valueExtractorMap["1genBosonPt"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson[0].node->p4.Pt(): UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBosonPz"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson[0].node->p4.Pz(): UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBosonEta"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson[0].node->p4.Eta(): UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBosonPhi"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson[0].node->p4.Phi(): UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBosonMass"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson[0].node->p4.mass(): UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBosonPdgId"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson[0].node->pdgId(): UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBosonStatus"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson[0].node->status(): UNDEFINED_VALUE;
	};



	
	// Boson daughters
	m_valueExtractorMap["1genBosonDaughterSize"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters.size(): UNDEFINED_VALUE;
	};


	// first daughter
	m_valueExtractorMap["1genBoson1DaughterPt"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].node->p4.Pt() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1DaughterPz"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].node->p4.Pz() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1DaughterEta"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].node->p4.Eta() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1DaughterPhi"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].node->p4.Phi() : UNDEFINED_VALUE;
	};
 	m_valueExtractorMap["1genBoson1DaughterMass"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].node->p4.mass() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1DaughterPdgId"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].node->pdgId() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1DaughterStatus"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].node->status() : UNDEFINED_VALUE;
	};

	// second daughter
	m_valueExtractorMap["1genBoson2DaughterPt"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].node->p4.Pt() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2DaughterPz"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].node->p4.Pz() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2DaughterEta"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].node->p4.Eta() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2DaughterPhi"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].node->p4.Phi() : UNDEFINED_VALUE;
	};
 	m_valueExtractorMap["1genBoson2DaughterMass"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].node->p4.mass() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2DaughterPdgId"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].node->pdgId() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2DaughterStatus"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].node->status() : UNDEFINED_VALUE;
	};


	// Boson granddaughters
	m_valueExtractorMap["1genBoson1DaughterGranddaughterSize"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>0) ? product.m_genBoson[0].Daughters[0].Daughters.size() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2DaughterGranddaughterSize"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>0) ? product.m_genBoson[0].Daughters[1].Daughters.size() : UNDEFINED_VALUE;
	};


	// first daughter daughters
	m_valueExtractorMap["1genBoson1Daughter1GranddaughterPt"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>0) ? product.m_genBoson[0].Daughters[0].Daughters[0].node->p4.Pt() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter1GranddaughterPz"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>0) ? product.m_genBoson[0].Daughters[0].Daughters[0].node->p4.Pz() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter1GranddaughterEta"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>0) ? product.m_genBoson[0].Daughters[0].Daughters[0].node->p4.Eta() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter1GranddaughterPhi"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>0) ? product.m_genBoson[0].Daughters[0].Daughters[0].node->p4.Phi() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter1GranddaughterMass"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>0) ? product.m_genBoson[0].Daughters[0].Daughters[0].node->p4.mass() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter1GranddaughterPdgId"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>0) ? product.m_genBoson[0].Daughters[0].Daughters[0].node->pdgId() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter1GranddaughterStatus"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>0) ? product.m_genBoson[0].Daughters[0].Daughters[0].node->status() : UNDEFINED_VALUE;
	};

	m_valueExtractorMap["1genBoson1Daughter2GranddaughterPt"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>1) ? product.m_genBoson[0].Daughters[0].Daughters[1].node->p4.Pt() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter2GranddaughterPz"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>1) ? product.m_genBoson[0].Daughters[0].Daughters[1].node->p4.Pz() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter2GranddaughterEta"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>1) ? product.m_genBoson[0].Daughters[0].Daughters[1].node->p4.Eta() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter2GranddaughterPhi"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>1) ? product.m_genBoson[0].Daughters[0].Daughters[1].node->p4.Phi() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter2GranddaughterMass"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>1) ? product.m_genBoson[0].Daughters[0].Daughters[1].node->p4.mass() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter2GranddaughterPdgId"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>1) ? product.m_genBoson[0].Daughters[0].Daughters[1].node->pdgId() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter2GranddaughterStatus"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>1) ? product.m_genBoson[0].Daughters[0].Daughters[1].node->status() : UNDEFINED_VALUE;
	};

	m_valueExtractorMap["1genBoson1Daughter3GranddaughterPt"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>2) ? product.m_genBoson[0].Daughters[0].Daughters[2].node->p4.Pt() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter3GranddaughterPz"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>2) ? product.m_genBoson[0].Daughters[0].Daughters[2].node->p4.Pz() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter3GranddaughterEta"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>2) ? product.m_genBoson[0].Daughters[0].Daughters[2].node->p4.Eta() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter3GranddaughterPhi"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>2) ? product.m_genBoson[0].Daughters[0].Daughters[2].node->p4.Phi() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter3GranddaughterMass"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>2) ? product.m_genBoson[0].Daughters[0].Daughters[2].node->p4.mass() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter3GranddaughterPdgId"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>2) ? product.m_genBoson[0].Daughters[0].Daughters[2].node->pdgId() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter3GranddaughterStatus"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>2) ? product.m_genBoson[0].Daughters[0].Daughters[2].node->status() : UNDEFINED_VALUE;
	};

	m_valueExtractorMap["1genBoson1Daughter4GranddaughterPt"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>3) ? product.m_genBoson[0].Daughters[0].Daughters[3].node->p4.Pt() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter4GranddaughterPz"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>3) ? product.m_genBoson[0].Daughters[0].Daughters[3].node->p4.Pz() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter4GranddaughterEta"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>3) ? product.m_genBoson[0].Daughters[0].Daughters[3].node->p4.Eta() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter4GranddaughterPhi"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>3) ? product.m_genBoson[0].Daughters[0].Daughters[3].node->p4.Phi() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter4GranddaughterMass"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>3) ? product.m_genBoson[0].Daughters[0].Daughters[3].node->p4.mass() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter4GranddaughterPdgId"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>3) ? product.m_genBoson[0].Daughters[0].Daughters[3].node->pdgId() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson1Daughter4GranddaughterStatus"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 0)&&(product.m_genBoson[0].Daughters[0].Daughters.size()>3) ? product.m_genBoson[0].Daughters[0].Daughters[3].node->status() : UNDEFINED_VALUE;
	};


	// second daughter daughters
	m_valueExtractorMap["1genBoson2Daughter1GranddaughterPt"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>0) ? product.m_genBoson[0].Daughters[1].Daughters[0].node->p4.Pt() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter1GranddaughterPz"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>0) ? product.m_genBoson[0].Daughters[1].Daughters[0].node->p4.Pz() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter1GranddaughterEta"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>0) ? product.m_genBoson[0].Daughters[1].Daughters[0].node->p4.Eta() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter1GranddaughterPhi"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>0) ? product.m_genBoson[0].Daughters[1].Daughters[0].node->p4.Phi() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter1GranddaughterMass"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>0) ? product.m_genBoson[0].Daughters[1].Daughters[0].node->p4.mass() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter1GranddaughterPdgId"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>0) ? product.m_genBoson[0].Daughters[1].Daughters[0].node->pdgId() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter1GranddaughterStatus"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>0) ? product.m_genBoson[0].Daughters[1].Daughters[0].node->status() : UNDEFINED_VALUE;
	};

	m_valueExtractorMap["1genBoson2Daughter2GranddaughterPt"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>1) ? product.m_genBoson[0].Daughters[1].Daughters[1].node->p4.Pt() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter2GranddaughterPz"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>1) ? product.m_genBoson[0].Daughters[1].Daughters[1].node->p4.Pz() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter2GranddaughterEta"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>1) ? product.m_genBoson[0].Daughters[1].Daughters[1].node->p4.Eta() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter2GranddaughterPhi"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>1) ? product.m_genBoson[0].Daughters[1].Daughters[1].node->p4.Phi() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter2GranddaughterMass"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>1) ? product.m_genBoson[0].Daughters[1].Daughters[1].node->p4.mass() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter2GranddaughterPdgId"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>1) ? product.m_genBoson[0].Daughters[1].Daughters[1].node->pdgId() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter2GranddaughterStatus"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>1) ? product.m_genBoson[0].Daughters[1].Daughters[1].node->status() : UNDEFINED_VALUE;
	};

	m_valueExtractorMap["1genBoson2Daughter3GranddaughterPt"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>2) ? product.m_genBoson[0].Daughters[1].Daughters[2].node->p4.Pt() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter3GranddaughterPz"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>2) ? product.m_genBoson[0].Daughters[1].Daughters[2].node->p4.Pz() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter3GranddaughterEta"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>2) ? product.m_genBoson[0].Daughters[1].Daughters[2].node->p4.Eta() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter3GranddaughterPhi"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>2) ? product.m_genBoson[0].Daughters[1].Daughters[2].node->p4.Phi() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter3GranddaughterMass"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>2) ? product.m_genBoson[0].Daughters[1].Daughters[2].node->p4.mass() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter3GranddaughterPdgId"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>2) ? product.m_genBoson[0].Daughters[1].Daughters[2].node->pdgId() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter3GranddaughterStatus"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>2) ? product.m_genBoson[0].Daughters[1].Daughters[2].node->status() : UNDEFINED_VALUE;
	};

	m_valueExtractorMap["1genBoson2Daughter4GranddaughterPt"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>3) ? product.m_genBoson[0].Daughters[1].Daughters[3].node->p4.Pt() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter4GranddaughterPz"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>3) ? product.m_genBoson[0].Daughters[1].Daughters[3].node->p4.Pz() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter4GranddaughterEta"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>3) ? product.m_genBoson[0].Daughters[1].Daughters[3].node->p4.Eta() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter4GranddaughterPhi"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>3) ? product.m_genBoson[0].Daughters[1].Daughters[3].node->p4.Phi() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter4GranddaughterMass"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>3) ? product.m_genBoson[0].Daughters[1].Daughters[3].node->p4.mass() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter4GranddaughterPdgId"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>3) ? product.m_genBoson[0].Daughters[1].Daughters[3].node->pdgId() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genBoson2Daughter4GranddaughterStatus"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (product.m_genBoson.size() > 0)&&(product.m_genBoson[0].Daughters.size() > 1)&&(product.m_genBoson[0].Daughters[1].Daughters.size()>3) ? product.m_genBoson[0].Daughters[1].Daughters[3].node->status() : UNDEFINED_VALUE;
	};


	LambdaNtupleConsumerBase<HttTypes>::Init(pset);
}

