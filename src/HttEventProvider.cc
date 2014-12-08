
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEventProvider.h"

/**
   \brief class to connect the analysis specific event content to the pipelines.
*/


HttEventProvider::HttEventProvider(FileInterface2 & fileInterface, InputTypeEnum inpType, bool batchMode) :
		KappaEventProvider<HttTypes>(fileInterface, inpType, batchMode)
{

}

void HttEventProvider::WireEvent(setting_type const& settings)
{
	KappaEventProvider::WireEvent(settings);
	
	// MET infos
	if(! settings.GetMvaMetTT().empty())
		this->m_event.m_mvaMetTT = this->SecureFileInterfaceGet<KMET>(settings.GetMvaMetTT());
	if(! settings.GetMvaMetMT().empty())
		this->m_event.m_mvaMetMT = this->SecureFileInterfaceGet<KMET>(settings.GetMvaMetMT());
	if(! settings.GetMvaMetET().empty())
		this->m_event.m_mvaMetET = this->SecureFileInterfaceGet<KMET>(settings.GetMvaMetET());
	if(! settings.GetMvaMetEM().empty())
		this->m_event.m_mvaMetEM = this->SecureFileInterfaceGet<KMET>(settings.GetMvaMetEM());
	
}

