
### Globals.
global debug env
global confFilePath
set debug 0
set noDupNames 0

### Load general Tcl package.
foreach p {struct textutil::split} {
	package require $p
}

if {[namespace exists TrafficGenerator] == 1} {
	::TrafficGenerator::clearObjectRecord
	::struct::record delete record ::TrafficGenerator::object_Record
	namespace delete TrafficGenerator
}

namespace eval TrafficGenerator {
	
	::struct::record define object_Record {name objRef type subType parent}
        
	variable XmlAttributes_Array
		array set XmlAttributes_Array {
			LOG ""
            DIR ""
			VERSION ""
            VERBOSE 3; # Error
        }
    variable LogFilePath ""
    variable ApiDirPath ""
    variable PkgVer ""
               
	variable objects_Array
	variable objectTypes_Array
	
	variable legacyObjectTypes_List {}
    
}

proc ::TrafficGenerator::GetObjectTypes {{type {}}} {
	variable objectTypes_Array
	variable legacyObjectTypes_List

	# If no specific type - return all types
	if {$type == {}} {
		return [array names objectTypes_Array]
	}

	# Validate type	
	if {[lsearch [array names objectTypes_Array] $type] == -1} {		
		# If type is not in the dynamic list, check if it is in the static (legacy) list for backward compatibility.
		# The only way we get here with static type is from GetObjectsByType so we simply have to return empty list.
		if {[lsearch $legacyObjectTypes_List $type] >= 0} {
			return {}
		} else {
			error "TSTclError - invalid type \{$type\}. Valid types are - [array names objectTypes_Array]"			
		}
	}
	
	# Return all sub types of the requested type
	return $objectTypes_Array($type)
}

#
# Auxiliary functions. Used only by other Tcl procedures (not called from driver builder).
#
	
proc ::TrafficGenerator::addToNameSpace {name object type {subType {}} {parent {}}} {
	global noDupNames
	variable objects_Array
	if {$noDupNames && [lsearch [array names objects_Array] $name] >= 0} {
		error "TSTclError - Duplicate name in configuration file - '$name' of type '$type'"
	}
	set id [array size objects_Array]
	set objects_Array($object) [::TrafficGenerator::object_Record ::TrafficGenerator::object_Record$id -name $name -objRef $object -type $type -subType $subType -parent $parent]
}
	
proc ::TrafficGenerator::array2list {pa {sl {}}} {
	upvar 1 $pa a 
	if {$sl == {}} {
		set sl [array names a]
	}
	set l {}
	if {[array size a] > 0} {
		foreach e $sl {
			lappend l [string trim $e\t$a($e)]\n
		}			
	}
	return ListDelimiter\n[join $l ""]
}
	
proc ::TrafficGenerator::clearObjectRecord {} {
	variable objects_Array
	variable objectTypes_Array
	foreach instance [::struct::record show instance ::TrafficGenerator::object_Record] {
		::struct::record delete instance $instance
	}
	array unset objects_Array
	array unset objectTypes_Array
}
	
proc ::TrafficGenerator::getObjects_Array {} {
	variable objects_Array
	set name2object_String {}
	foreach objRef [array names objects_Array] {
		append name2object_String $objRef\t[join [$objects_Array($objRef) cget] \t]\n
	}
	return [string trim $name2object_String]
}

proc ::TrafficGenerator::setAllObjectTypes {{legacyObjectTypes {}}} {
	variable objects_Array
	variable objectTypes_Array
	variable legacyObjectTypes_List
	foreach objType [array names objects_Array] {
		lappend objectTypes_Array([$objects_Array($objType) cget -type]) [$objects_Array($objType) cget -subType]
	}
	foreach objType [array names objectTypes_Array] {
		set objectTypes_Array($objType) [::struct::list flatten [lsort -unique $objectTypes_Array($objType)]]
	}
	set legacyObjectTypes_List $legacyObjectTypes
}
