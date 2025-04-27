/*
 INSPIIIIIIIIIREDDDDDDDD
 */

/*global window, tizen, console*/

/**
 * Main application module.
 * Provides a namespace for other application modules.
 * Handles application life cycle.
 *
 * @module app
 * @requires {@link app.model}
 * @requires {@link app.ui}
 * @namespace app
 */

window.app = window.app || {};

// strict mode wrapper
(function defineApp(app) {
    'use strict';

    /**
     * Exits application.
     *
     * @memberof app
     * @public
     */
    function exitApplication() {
        try {
            tizen.application.getCurrentApplication().exit();
        } catch (e) {
            console.error('Error:', e.message);
        }
    }

    /**
     * Handles tizenhwkey event.
     *
     * @memberof app
     * @private
     * @param {Event} event
     */
    function onHardwareKeysTap(event) {
        if (event.keyName === 'back') {
            exitApplication();
        }
    }

    /**
     * Binds events.
     *
     * @memberof app
     * @private
     */
    function bindEvents() {
        window.addEventListener('tizenhwkey', onHardwareKeysTap);
    }

    /**
     * Initializes application.
     *
     * @memberof app
     * @private
     */
    function init() {
        bindEvents();

        app.model.init();
        app.ui.init();

    }

    window.addEventListener('load', init);
}(window.app));