set dir  {C:/Program Files (x86)/Spirent Communications/Spirent TestCenter 4.64/Spirent TestCenter Application} 
source  {C:/Program Files (x86)/Spirent Communications/Spirent TestCenter 4.64/Spirent TestCenter Application/pkgIndex.tcl} 
package require SpirentTestCenter
stc::get system1 -children-automationoptions
stc::get automationoptions -name
stc::config automationoptions -LogLevel  {ERROR} 
stc::create project -under system1 
stc::get project1 -name
stc::perform ResetConfig -config  {system1} 
set dir  {C:/Program Files (x86)/Spirent Communications/Spirent TestCenter 4.64/Spirent TestCenter Application} 
source  {C:/Program Files (x86)/Spirent Communications/Spirent TestCenter 4.64/Spirent TestCenter Application/pkgIndex.tcl} 
package require SpirentTestCenter
stc::get system1 -children-automationoptions
stc::get automationoptions -name
stc::config automationoptions -LogLevel  {ERROR} 
stc::create project -under system1 
stc::get project1 -name
stc::perform ResetConfig -config  {system1} 
