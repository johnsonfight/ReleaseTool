/** @file
    Header file contains system BIOS version, build dates, and other information.

    Copyright (c) 2013 - 2015 Dell Inc.

    This program contains proprietary and confidential information.
    All rights reserved.

**/

#ifndef _DELL_BIOS_VERSION_H_
#define _DELL_BIOS_VERSION_H_
#include <DellGenericMacros.h>

/// ****************************************************************************
///   _     ___     ____  _____   ___    _________           __           ___
///  (_)  .' ..]   |_   \|_   _|.'   `. |  _   _  |         |  ]        .' ..]
///  __  _| |_       |   \ | | /  .-.  \|_/ | | \_|     .--.| | .---.  _| |_
/// [  |'-| |-'      | |\ \| | | |   | |    | |       / /'`\' |/ /__\\'-| |-'
///  | |  | |       _| |_\   |_\  `-'  /   _| |_      | \__/  || \__.,  | |
/// [___][___]     |_____|\____|`.___.'   |_____|      '.__.;__]'.__.' [___]
///
/// ****************************************************************************

#ifdef ESI_MORMONT
// ESI Mormont versioning
// BIOS version numbers in X.Y.Z format. X,Y, and Z must be within 0 to 99
//
#define DELL_BIOS_MAJOR_VERSION       1        // Major release version number
#define DELL_BIOS_MINOR_VERSION       5        // Minor release version number
#define DELL_BIOS_MAIN_VERSION        4        // Main release version number

// The Minimum Compatible BIOS version is the minimum version that this BIOS
// can be updated from without forcing -wipeclean.  If the current running BIOS
// in the target system is lower (older) than the version below, -wipeclean will
// be forced when updating to this BIOS.
#define DELL_MINIMUM_COMPATIBLE_BIOS_MAJOR_VERSION  0
#define DELL_MINIMUM_COMPATIBLE_BIOS_MINOR_VERSION  0
#define DELL_MINIMUM_COMPATIBLE_BIOS_MAIN_VERSION   0

//
// Optional build label. Use "" for released version of BIOS. Uncomment this out for your test BIOS
//
#ifndef BUILDING_RECOVERY_BIOS
#if ODM_BUILD
#define DELL_BIOS_BUILD_OPTIONAL_INFO_STR       L"ODM BIOS"
#else
#ifndef BUILDING_RELEASE_BIOS
#define DELL_BIOS_BUILD_OPTIONAL_INFO_STR       L"OEM BIOS"
#else
#define DELL_BIOS_BUILD_OPTIONAL_INFO_STR       L""
#endif
#endif
#else
#define DELL_BIOS_BUILD_OPTIONAL_INFO_STR       L"Recovery BIOS"
#endif

//
// Build Date
//
#define DELL_BIOS_BUILD_MONTH         7         // month without leading 0 (1 to 12)
#define DELL_BIOS_BUILD_DAY           31        // day without leading 0 (1 to 31)
#define DELL_BIOS_BUILD_YEAR          18        // last 2 digits of the year (0 to 99)
                                                //
//
// Feature Capability Flag
// Bit [14:0] - Feature Capability Flag
// Bit [15] - is reserved for OEM usage only and should NOT be set (always 0)

#define PRODUCTION_FUSED_PCH          BIT0      // BIT0 = 1 ; PCH is fused as production (QS vs. Engineering Sample).
#define BTG_KEY_VERSION_UPDATE1       BIT1      // BIT0 = 1 ; A-rev BootGuard Key version. Don't allow flashing to a BIOS before this.
#define DIMM_IS_18NM                  BIT2      // BIT2 = 1 ; 18nm DIMMs are installed in 2DPC config, and DDR speed is 2666 or more.
#define CASCADE_CPU_PRESENT           BIT3      // BIT3 = 1 ; Cascade Lake CPU support
#define BIOS_FEATURE_FLAG             PRODUCTION_FUSED_PCH + BTG_KEY_VERSION_UPDATE1 + DIMM_IS_18NM + CASCADE_CPU_PRESENT// Feature capability flag
#else
#ifdef ESI_LUMINOR
// ESI Luminor versioning
// BIOS version numbers in X.Y.Z format. X,Y, and Z must be within 0 to 99
//
#define DELL_BIOS_MAJOR_VERSION       0        // Major release version number
#define DELL_BIOS_MINOR_VERSION       1        // Minor release version number
#define DELL_BIOS_MAIN_VERSION        0        // Main release version number

// The Minimum Compatible BIOS version is the minimum version that this BIOS
// can be updated from without forcing -wipeclean.  If the current running BIOS
// in the target system is lower (older) than the version below, -wipeclean will
// be forced when updating to this BIOS.
#define DELL_MINIMUM_COMPATIBLE_BIOS_MAJOR_VERSION  0
#define DELL_MINIMUM_COMPATIBLE_BIOS_MINOR_VERSION  0
#define DELL_MINIMUM_COMPATIBLE_BIOS_MAIN_VERSION   0

//
// Optional build label. Use "" for released version of BIOS. Uncomment this out for your test BIOS
//
#ifndef BUILDING_RECOVERY_BIOS
#if ODM_BUILD
#define DELL_BIOS_BUILD_OPTIONAL_INFO_STR       L"ODM BIOS"
#else
#ifndef BUILDING_RELEASE_BIOS
#define DELL_BIOS_BUILD_OPTIONAL_INFO_STR       L"OEM BIOS"
#else
#define DELL_BIOS_BUILD_OPTIONAL_INFO_STR       L""
#endif
#endif
#else
#define DELL_BIOS_BUILD_OPTIONAL_INFO_STR       L"Recovery BIOS"
#endif

//
// Build Date
//
#define DELL_BIOS_BUILD_MONTH         7         // month without leading 0 (1 to 12)
#define DELL_BIOS_BUILD_DAY           31        // day without leading 0 (1 to 31)
#define DELL_BIOS_BUILD_YEAR          18        // last 2 digits of the year (0 to 99)
                                                //
//
// Feature Capability Flag
// Bit [14:0] - Feature Capability Flag
// Bit [15] - is reserved for OEM usage only and should NOT be set (always 0)

#define PRODUCTION_FUSED_PCH          BIT0      // BIT0 = 1 ; PCH is fused as production (QS vs. Engineering Sample).
#define BTG_KEY_VERSION_UPDATE1       BIT1      // BIT0 = 1 ; A-rev BootGuard Key version. Don't allow flashing to a BIOS before this.
#define DIMM_IS_18NM                  BIT2      // BIT2 = 1 ; 18nm DIMMs are installed in 2DPC config, and DDR speed is 2666 or more.
#define CASCADE_CPU_PRESENT           BIT3      // BIT3 = 1 ; Cascade Lake CPU support
#define BIOS_FEATURE_FLAG             PRODUCTION_FUSED_PCH + BTG_KEY_VERSION_UPDATE1 + DIMM_IS_18NM + CASCADE_CPU_PRESENT// Feature capability flag
#else
// Taurus version
// BIOS version numbers in X.Y.Z format. X,Y, and Z must be within 0 to 99
//
#define DELL_BIOS_MAJOR_VERSION       2
#define DELL_BIOS_MINOR_VERSION       7
#define DELL_BIOS_MAIN_VERSION        4

// The Minimum Compatible BIOS version is the minimum version that this BIOS
// can be updated from without forcing -wipeclean.  If the current running BIOS
// in the target system is lower (older) than the version below, -wipeclean will
// be forced when updating to this BIOS.
#define DELL_MINIMUM_COMPATIBLE_BIOS_MAJOR_VERSION  0
#define DELL_MINIMUM_COMPATIBLE_BIOS_MINOR_VERSION  0
#define DELL_MINIMUM_COMPATIBLE_BIOS_MAIN_VERSION   0

//
// Optional build label. Use "" for released version of BIOS. Uncomment this out for your test BIOS
//
#ifndef BUILDING_RECOVERY_BIOS
#if ODM_BUILD
#define DELL_BIOS_BUILD_OPTIONAL_INFO_STR       L"ODM BIOS"
#else
#ifndef BUILDING_RELEASE_BIOS
#define DELL_BIOS_BUILD_OPTIONAL_INFO_STR       L"OEM BIOS"
#else
#define DELL_BIOS_BUILD_OPTIONAL_INFO_STR       L""
#endif
#endif
#else
#define DELL_BIOS_BUILD_OPTIONAL_INFO_STR       L"Recovery BIOS"
#endif

//
// Build Date
//
#define DELL_BIOS_BUILD_MONTH         4
#define DELL_BIOS_BUILD_DAY           26
#define DELL_BIOS_BUILD_YEAR          20
                                                //
//
// Feature Capability Flag
// Bit [14:0] - Feature Capability Flag
// Bit [15] - is reserved for OEM usage only and should NOT be set (always 0)

#define PRODUCTION_FUSED_PCH          BIT0      // BIT0 = 1 ; PCH is fused as production (QS vs. Engineering Sample).
#define BTG_KEY_VERSION_UPDATE1       BIT1      // BIT0 = 1 ; A-rev BootGuard Key version. Don't allow flashing to a BIOS before this.
#define DIMM_IS_18NM                  BIT2      // BIT2 = 1 ; 18nm DIMMs are installed in 2DPC config, and DDR speed is 2666 or more.
#define CASCADE_CPU_PRESENT           BIT3      // BIT3 = 1 ; Cascade Lake CPU support
#define BIOS_FEATURE_FLAG             PRODUCTION_FUSED_PCH + BTG_KEY_VERSION_UPDATE1 + DIMM_IS_18NM + CASCADE_CPU_PRESENT// Feature capability flag
#endif
#endif

// =====================================================================================
//               Below code should NOT be modified from release to release
// -------------------------------------------------------------------------------------
//
// Make sure the optional build label is not too long and cause display issues and potential RSODs
//
#ifdef DELL_BIOS_BUILD_OPTIONAL_INFO_STR
static CHAR16 LabelStrTmp[32] = DELL_BIOS_BUILD_OPTIONAL_INFO_STR; // A trick to make sure the label doesn't get insanely long
#endif
//
// Make sure the version numbers are valid
//
#if (DELL_BIOS_MAJOR_VERSION > 99 ||DELL_BIOS_MINOR_VERSION > 99 || DELL_BIOS_MAIN_VERSION > 99)
#error Invalid Version Numbers!
#endif
//
// The BIOS Version Name Spec has this 49.0.48 on the blacklist
//
#if (DELL_BIOS_MAJOR_VERSION == 49 && DELL_BIOS_MINOR_VERSION == 0 && DELL_BIOS_MAIN_VERSION == 48)
#error Blacklisted Version Number is used!
#endif
//
// Make sure the build dates are sane
//
#if (DELL_BIOS_BUILD_MONTH > 12 || DELL_BIOS_BUILD_MONTH < 1)
#error Build Month Out of Range!
#endif

#if (DELL_BIOS_BUILD_DAY > 31 || DELL_BIOS_BUILD_DAY < 1)
#error Build Day Out of Range!
#endif

#if (DELL_BIOS_BUILD_YEAR > 99)
#error Build Year Out of Range!
#endif

//
// The following will automatically generate the version string
//
#define DELL_BIOS_VERSION_STR        L_STR(MKSTR(DELL_BIOS_MAJOR_VERSION)) \
                                     L"." \
                                     L_STR(MKSTR(DELL_BIOS_MINOR_VERSION)) \
                                     L"." \
                                     L_STR(MKSTR(DELL_BIOS_MAIN_VERSION))

//
// The following will automatically generate the ASCII build date string. The format must be
// in the form of mm/dd/yy. It must contain exactly 8 characters. A forward slash '/' must
// separate the month from the day and the day from the year.
//
#define DELL_BIOS_BUILD_MONTH_ASCII MKSTR(DELL_BIOS_BUILD_MONTH/10) \
                                    MKSTR(DELL_BIOS_BUILD_MONTH%10)

#define DELL_BIOS_BUILD_DAY_ASCII   MKSTR(DELL_BIOS_BUILD_DAY/10) \
                                    MKSTR(DELL_BIOS_BUILD_DAY%10)

#define DELL_BIOS_BUILD_YEAR_ASCII  MKSTR(DELL_BIOS_BUILD_YEAR/10) \
                                    MKSTR(DELL_BIOS_BUILD_YEAR%10)
#pragma message (TODO (Wei) "CSM BIOS compatibilty region needs to have this build date string")

// Compute BIOS_DATE_STR which is used by Platform ID DPI:
#if (DELL_BIOS_BUILD_MONTH < 10)
# define TWODIGMONTH L"0" L_STR(MKSTR(DELL_BIOS_BUILD_MONTH))
#else
# define TWODIGMONTH L_STR(MKSTR(DELL_BIOS_BUILD_MONTH))
#endif

#if (DELL_BIOS_BUILD_DAY < 10)
# define TWODIGDAY L"0" L_STR(MKSTR(DELL_BIOS_BUILD_DAY))
#else
# define TWODIGDAY L_STR(MKSTR(DELL_BIOS_BUILD_DAY))
#endif

#define BIOS_DATE_STR TWODIGMONTH L"/" TWODIGDAY L"/20" L_STR(MKSTR(DELL_BIOS_BUILD_YEAR))

#endif














