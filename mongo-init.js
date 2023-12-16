db.createUser({
    user: "test_user",
    pwd: "test_password",
    roles: [
        {
            role: 'readWrite',
            db: "test_db"
        }
    ]
});

function _getEnv(varName) {
    return db.adminCommand({ getParameter: 1, ["process.env." + varName]: 1 })["process.env." + varName];
}