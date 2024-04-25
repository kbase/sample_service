
package us.kbase.sampleservice;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: UpdateSampleACLsParams</p>
 * <pre>
 * update_sample_acls parameters.
 *         id - the ID of the sample to modify.
 *         admin - a list of users that will receive admin privileges. Default none.
 *         write - a list of users that will receive write privileges. Default none.
 *         read - a list of users that will receive read privileges. Default none.
 *         remove - a list of users that will have all privileges removed. Default none.
 *         public_read - an integer that determines whether the sample will be set to publicly
 *             readable:
 *             > 0: public read.
 *             0: No change (the default).
 *             < 0: private.
 *         at_least - false, the default, indicates that the users should get the exact permissions
 *             as specified in the user lists, which may mean a reduction in permissions. If true,
 *             users that already exist in the sample ACLs will not have their permissions reduced
 *             as part of the ACL update unless they are in the remove list. E.g. if a user has
 *             write permissions and read permissions are specified in the update, no changes will
 *             be made to the user's permission.
 *         as_admin - update the sample acls regardless of sample ACL contents as long as the user has
 *             full service administration permissions.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "id",
    "admin",
    "write",
    "read",
    "remove",
    "public_read",
    "at_least",
    "as_admin"
})
public class UpdateSampleACLsParams {

    @JsonProperty("id")
    private java.lang.String id;
    @JsonProperty("admin")
    private List<String> admin;
    @JsonProperty("write")
    private List<String> write;
    @JsonProperty("read")
    private List<String> read;
    @JsonProperty("remove")
    private List<String> remove;
    @JsonProperty("public_read")
    private Long publicRead;
    @JsonProperty("at_least")
    private Long atLeast;
    @JsonProperty("as_admin")
    private Long asAdmin;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("id")
    public java.lang.String getId() {
        return id;
    }

    @JsonProperty("id")
    public void setId(java.lang.String id) {
        this.id = id;
    }

    public UpdateSampleACLsParams withId(java.lang.String id) {
        this.id = id;
        return this;
    }

    @JsonProperty("admin")
    public List<String> getAdmin() {
        return admin;
    }

    @JsonProperty("admin")
    public void setAdmin(List<String> admin) {
        this.admin = admin;
    }

    public UpdateSampleACLsParams withAdmin(List<String> admin) {
        this.admin = admin;
        return this;
    }

    @JsonProperty("write")
    public List<String> getWrite() {
        return write;
    }

    @JsonProperty("write")
    public void setWrite(List<String> write) {
        this.write = write;
    }

    public UpdateSampleACLsParams withWrite(List<String> write) {
        this.write = write;
        return this;
    }

    @JsonProperty("read")
    public List<String> getRead() {
        return read;
    }

    @JsonProperty("read")
    public void setRead(List<String> read) {
        this.read = read;
    }

    public UpdateSampleACLsParams withRead(List<String> read) {
        this.read = read;
        return this;
    }

    @JsonProperty("remove")
    public List<String> getRemove() {
        return remove;
    }

    @JsonProperty("remove")
    public void setRemove(List<String> remove) {
        this.remove = remove;
    }

    public UpdateSampleACLsParams withRemove(List<String> remove) {
        this.remove = remove;
        return this;
    }

    @JsonProperty("public_read")
    public Long getPublicRead() {
        return publicRead;
    }

    @JsonProperty("public_read")
    public void setPublicRead(Long publicRead) {
        this.publicRead = publicRead;
    }

    public UpdateSampleACLsParams withPublicRead(Long publicRead) {
        this.publicRead = publicRead;
        return this;
    }

    @JsonProperty("at_least")
    public Long getAtLeast() {
        return atLeast;
    }

    @JsonProperty("at_least")
    public void setAtLeast(Long atLeast) {
        this.atLeast = atLeast;
    }

    public UpdateSampleACLsParams withAtLeast(Long atLeast) {
        this.atLeast = atLeast;
        return this;
    }

    @JsonProperty("as_admin")
    public Long getAsAdmin() {
        return asAdmin;
    }

    @JsonProperty("as_admin")
    public void setAsAdmin(Long asAdmin) {
        this.asAdmin = asAdmin;
    }

    public UpdateSampleACLsParams withAsAdmin(Long asAdmin) {
        this.asAdmin = asAdmin;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((((((((((((("UpdateSampleACLsParams"+" [id=")+ id)+", admin=")+ admin)+", write=")+ write)+", read=")+ read)+", remove=")+ remove)+", publicRead=")+ publicRead)+", atLeast=")+ atLeast)+", asAdmin=")+ asAdmin)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
