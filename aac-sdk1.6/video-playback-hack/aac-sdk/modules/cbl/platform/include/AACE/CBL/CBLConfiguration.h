/*
 * Copyright 2017-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */

#ifndef AACE_CBL_CBL_CONFIGURATION_H
#define AACE_CBL_CBL_CONFIGURATION_H

#include "AACE/Core/EngineConfiguration.h"

/** @file */

namespace aace {
namespace cbl {
namespace config {
 
/**
 * The @c CBLConfiguration class is a factory interface for creating CBL service configuration objects.
 */
class CBLConfiguration {
public:
    /**
     * Factory method used to programmatically generate cbl configuration data.
     * The data generated by this method is equivalent to providing the following JSON
     * values in a configuration file:
     *
     * @code{.json}
     * {
     *   "aace.cbl": {
     *     "requestTimeout": <REQUEST_TIMEOUT_IN_SECONDS> 
     *   }
     * }
     * @endcode
     *
     * @param [in] requestTimeout The timeout used for requesting code pair
     * 
     * The default configuration of 60 seconds will be overriden with this value when configured.
     */
    static std::shared_ptr<aace::core::config::EngineConfiguration> createCBLConfig( const int seconds );
};

} // aace::cbl::config
} // aace::cbl
} // aace

#endif