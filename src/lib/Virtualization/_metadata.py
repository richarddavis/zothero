# This file is generated by objective.metadata
#
# Last update: Sun Feb 20 19:29:05 2022
#
# flake8: noqa

import objc, sys
from typing import NewType

if sys.maxsize > 2**32:

    def sel32or64(a, b):
        return b

else:

    def sel32or64(a, b):
        return a


if objc.arch == "arm64":

    def selAorI(a, b):
        return a

else:

    def selAorI(a, b):
        return b


misc = {}
constants = """$VZErrorDomain$"""
enums = """$VZDiskImageCachingModeAutomatic@0$VZDiskImageCachingModeCached@2$VZDiskImageCachingModeUncached@1$VZDiskImageSynchronizationModeFsync@2$VZDiskImageSynchronizationModeFull@1$VZDiskImageSynchronizationModeNone@3$VZErrorInternal@1$VZErrorInvalidDiskImage@5$VZErrorInvalidVirtualMachineConfiguration@2$VZErrorInvalidVirtualMachineState@3$VZErrorInvalidVirtualMachineStateTransition@4$VZErrorVirtualMachineLimitExceeded@6$VZMacAuxiliaryStorageInitializationOptionAllowOverwrite@1$VZVirtualMachineStateError@3$VZVirtualMachineStatePaused@2$VZVirtualMachineStatePausing@5$VZVirtualMachineStateResuming@6$VZVirtualMachineStateRunning@1$VZVirtualMachineStateStarting@4$VZVirtualMachineStateStopped@0$VZVirtualMachineStateStopping@7$"""
misc.update(
    {
        "VZMacAuxiliaryStorageInitializationOptions": NewType(
            "VZMacAuxiliaryStorageInitializationOptions", int
        ),
        "VZDiskImageSynchronizationMode": NewType(
            "VZDiskImageSynchronizationMode", int
        ),
        "VZDiskImageCachingMode": NewType("VZDiskImageCachingMode", int),
        "VZErrorCode": NewType("VZErrorCode", int),
        "VZVirtualMachineState": NewType("VZVirtualMachineState", int),
    }
)
misc.update({})
r = objc.registerMetaDataForSelector
objc._updatingMetadata(True)
try:
    r(
        b"NSObject",
        b"guestDidStopVirtualMachine:",
        {"required": False, "retval": {"type": b"v"}, "arguments": {2: {"type": b"@"}}},
    )
    r(
        b"NSObject",
        b"listener:shouldAcceptNewConnection:fromSocketDevice:",
        {
            "required": False,
            "retval": {"type": b"Z"},
            "arguments": {2: {"type": b"@"}, 3: {"type": b"@"}, 4: {"type": b"@"}},
        },
    )
    r(
        b"NSObject",
        b"virtualMachine:didStopWithError:",
        {
            "required": False,
            "retval": {"type": b"v"},
            "arguments": {2: {"type": b"@"}, 3: {"type": b"@"}},
        },
    )
    r(
        b"NSObject",
        b"virtualMachine:networkDevice:attachmentWasDisconnectedWithError:",
        {
            "required": False,
            "retval": {"type": b"v"},
            "arguments": {2: {"type": b"@"}, 3: {"type": b"@"}, 4: {"type": b"@"}},
        },
    )
    r(
        b"VZDiskImageStorageDeviceAttachment",
        b"initWithURL:readOnly:cachingMode:synchronizationMode:error:",
        {"arguments": {3: {"type": b"Z"}, 6: {"type_modifier": b"o"}}},
    )
    r(
        b"VZDiskImageStorageDeviceAttachment",
        b"initWithURL:readOnly:error:",
        {"arguments": {3: {"type": b"Z"}, 4: {"type_modifier": b"o"}}},
    )
    r(b"VZDiskImageStorageDeviceAttachment", b"isReadOnly", {"retval": {"type": "Z"}})
    r(b"VZFileSerialPortAttachment", b"append", {"retval": {"type": b"Z"}})
    r(
        b"VZFileSerialPortAttachment",
        b"initWithURL:append:error:",
        {"arguments": {3: {"type": b"Z"}, 4: {"type_modifier": b"o"}}},
    )
    r(b"VZMACAddress", b"isBroadcastAddress", {"retval": {"type": b"Z"}})
    r(b"VZMACAddress", b"isLocallyAdministeredAddress", {"retval": {"type": b"Z"}})
    r(b"VZMACAddress", b"isMulticastAddress", {"retval": {"type": b"Z"}})
    r(b"VZMACAddress", b"isUnicastAddress", {"retval": {"type": b"Z"}})
    r(b"VZMACAddress", b"isUniversallyAdministeredAddress", {"retval": {"type": b"Z"}})
    r(
        b"VZMacAuxiliaryStorage",
        b"initCreatingStorageAtURL:hardwareModel:options:error:",
        {"arguments": {5: {"type_modifier": b"o"}}},
    )
    r(b"VZMacHardwareModel", b"isSupported", {"retval": {"type": b"Z"}})
    r(
        b"VZMacOSInstaller",
        b"installWithCompletionHandler:",
        {
            "arguments": {
                2: {
                    "callable": {
                        "retval": {"type": b"v"},
                        "arguments": {0: {"type": b"^v"}, 1: {"type": b"@"}},
                    }
                }
            }
        },
    )
    r(
        b"VZMacOSRestoreImage",
        b"fetchLatestSupportedWithCompletionHandler:",
        {
            "arguments": {
                2: {
                    "callable": {
                        "retval": {"type": b"v"},
                        "arguments": {
                            0: {"type": b"^v"},
                            1: {"type": b"@"},
                            2: {"type": b"@"},
                        },
                    }
                }
            }
        },
    )
    r(
        b"VZMacOSRestoreImage",
        b"loadFileURL:completionHandler:",
        {
            "arguments": {
                3: {
                    "callable": {
                        "retval": {"type": b"v"},
                        "arguments": {
                            0: {"type": b"^v"},
                            1: {"type": b"@"},
                            2: {"type": b"@"},
                        },
                    }
                }
            }
        },
    )
    r(
        b"VZMacOSRestoreImage",
        b"operatingSystemVersion",
        {"retval": {"type": b"{_NSOperatingSystemVersion=qqq}"}},
    )
    r(
        b"VZMultipleDirectoryShare",
        b"validateName:error:",
        {"retval": {"type": b"Z"}, "arguments": {3: {"type_modifier": b"o"}}},
    )
    r(
        b"VZSharedDirectory",
        b"initWithURL:readOnly:",
        {"arguments": {3: {"type": b"Z"}}},
    )
    r(b"VZSharedDirectory", b"isReadOnly", {"retval": {"type": b"Z"}})
    r(
        b"VZVirtioBlockDeviceConfiguration",
        b"validateBlockDeviceIdentifier:error:",
        {"retval": {"type": b"Z"}, "arguments": {3: {"type_modifier": b"o"}}},
    )
    r(
        b"VZVirtioFileSystemDeviceConfiguration",
        b"validateTag:error:",
        {"retval": {"type": b"Z"}, "arguments": {3: {"type_modifier": b"o"}}},
    )
    r(
        b"VZVirtioSocketDevice",
        b"connectToPort:completionHandler:",
        {
            "arguments": {
                3: {
                    "callable": {
                        "retval": {"type": b"v"},
                        "arguments": {
                            0: {"type": b"^v"},
                            1: {"type": b"@"},
                            2: {"type": b"@"},
                        },
                    }
                }
            }
        },
    )
    r(b"VZVirtualMachine", b"canPause", {"retval": {"type": b"Z"}})
    r(b"VZVirtualMachine", b"canRequestStop", {"retval": {"type": b"Z"}})
    r(b"VZVirtualMachine", b"canResume", {"retval": {"type": b"Z"}})
    r(b"VZVirtualMachine", b"canStart", {"retval": {"type": b"Z"}})
    r(b"VZVirtualMachine", b"canStop", {"retval": {"type": b"Z"}})
    r(b"VZVirtualMachine", b"isSupported", {"retval": {"type": b"Z"}})
    r(
        b"VZVirtualMachine",
        b"pauseWithCompletionHandler:",
        {
            "arguments": {
                2: {
                    "callable": {
                        "retval": {"type": b"v"},
                        "arguments": {0: {"type": b"^v"}, 1: {"type": b"@"}},
                    }
                }
            }
        },
    )
    r(
        b"VZVirtualMachine",
        b"requestStopWithError:",
        {"retval": {"type": b"Z"}, "arguments": {2: {"type_modifier": b"o"}}},
    )
    r(
        b"VZVirtualMachine",
        b"resumeWithCompletionHandler:",
        {
            "arguments": {
                2: {
                    "callable": {
                        "retval": {"type": b"v"},
                        "arguments": {0: {"type": b"^v"}, 1: {"type": b"@"}},
                    }
                }
            }
        },
    )
    r(
        b"VZVirtualMachine",
        b"startWithCompletionHandler:",
        {
            "arguments": {
                2: {
                    "callable": {
                        "retval": {"type": b"v"},
                        "arguments": {0: {"type": b"^v"}, 1: {"type": b"@"}},
                    }
                }
            }
        },
    )
    r(
        b"VZVirtualMachine",
        b"stopWithCompletionHandler:",
        {
            "arguments": {
                2: {
                    "callable": {
                        "retval": {"type": b"v"},
                        "arguments": {0: {"type": b"^v"}, 1: {"type": b"@"}},
                    }
                }
            }
        },
    )
    r(
        b"VZVirtualMachineConfiguration",
        b"validateWithError:",
        {"retval": {"type": b"Z"}, "arguments": {2: {"type_modifier": b"o"}}},
    )
    r(b"VZVirtualMachineView", b"capturesSystemKeys", {"retval": {"type": b"Z"}})
    r(
        b"VZVirtualMachineView",
        b"setCapturesSystemKeys:",
        {"arguments": {2: {"type": b"Z"}}},
    )
finally:
    objc._updatingMetadata(False)
expressions = {}

# END OF FILE