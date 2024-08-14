/* @odoo-module */
import publicWidget from 'web.public.widget';

publicWidget.registry.SiiChileLogin = publicWidget.Widget.extend({
    selector: '#wrapwrap',

    events: {
        'click a#siiLoginLink': '_onLoginLinkClick',
        'click #loginForm input[type="button"]': '_onLoginButtonClick',
    },

    _onLoginLinkClick: function (ev) {
        ev.preventDefault();
        this._showLoginForm();
    },

    _showLoginForm: function () {
        document.getElementById('loginForm').style.display = 'block';
    },

    _onLoginButtonClick: function () {
        const rut = document.getElementById('rut').value;
        const password = document.getElementById('siipassword').value;

        const xhr = new XMLHttpRequest();
        xhr.open("POST", "https://app.ssichile.cl/login", true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                alert("Login successful! You can now go to 'Consultas Históricas' to download your data.");
            } else if (xhr.readyState === 4) {
                alert("Login failed: " + xhr.responseText);
            }
        };
        xhr.send("email=jlasen@soothsayerinsurance.com&password=Soot2024.");
    },
});
