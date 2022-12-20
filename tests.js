function isBase64(str) {
    if (str ==='' || str.trim() ===''){ return false; }
    try {
        return btoa(atob(str)) == str;
    } catch (err) {
        return false;
    }
}

console.log(isBase64("PK12+bMd8BQtDRpjmBCS79twPpRVXFAwSZ3RDfuDGosh+Zt5IgS82V4S9LMs19r0/o0HCq8Go+S0lwUBL+GcTA=="))