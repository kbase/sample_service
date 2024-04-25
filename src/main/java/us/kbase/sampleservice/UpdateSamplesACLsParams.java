
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
 * <p>Original spec-file type: UpdateSamplesACLsParams</p>
 * <pre>
 * update_samples_acls parameters.
 *         These parameters are the same as update_sample_acls, except:
 *         ids - a list of IDs of samples to modify.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "ids",
    "admin",
    "write",
    "read",
    "remove",
    "public_read",
    "at_least",
    "as_admin"
})
public class UpdateSamplesACLsParams {

    @JsonProperty("ids")
    private List<String> ids;
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

    @JsonProperty("ids")
    public List<String> getIds() {
        return ids;
    }

    @JsonProperty("ids")
    public void setIds(List<String> ids) {
        this.ids = ids;
    }

    public UpdateSamplesACLsParams withIds(List<String> ids) {
        this.ids = ids;
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

    public UpdateSamplesACLsParams withAdmin(List<String> admin) {
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

    public UpdateSamplesACLsParams withWrite(List<String> write) {
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

    public UpdateSamplesACLsParams withRead(List<String> read) {
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

    public UpdateSamplesACLsParams withRemove(List<String> remove) {
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

    public UpdateSamplesACLsParams withPublicRead(Long publicRead) {
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

    public UpdateSamplesACLsParams withAtLeast(Long atLeast) {
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

    public UpdateSamplesACLsParams withAsAdmin(Long asAdmin) {
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
        return ((((((((((((((((((("UpdateSamplesACLsParams"+" [ids=")+ ids)+", admin=")+ admin)+", write=")+ write)+", read=")+ read)+", remove=")+ remove)+", publicRead=")+ publicRead)+", atLeast=")+ atLeast)+", asAdmin=")+ asAdmin)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
