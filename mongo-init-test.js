db.createUser({
    user: process.env.MONGO_INITDB_ROOT_USERNAME,
    pwd: process.env.MONGO_INITDB_ROOT_PASSWORD,
    roles: [
        {
            role: 'readWrite',
            db: process.env.MONGO_DB_NAME
        }
    ]
});

function _getEnv(varName) {
    return db.adminCommand({ getParameter: 1, ["process.env." + varName]: 1 })["process.env." + varName];
}