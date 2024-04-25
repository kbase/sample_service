
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
 * <p>Original spec-file type: SampleACLs</p>
 * <pre>
 * Access control lists for a sample. Access levels include the privileges of the lower
 * access levels.
 * owner - the user that created and owns the sample.
 * admin - users that can administrate (e.g. alter ACLs) the sample.
 * write - users that can write (e.g. create a new version) to the sample.
 * read - users that can view the sample.
 * public_read - whether any user can read the sample, regardless of permissions.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "owner",
    "admin",
    "write",
    "read",
    "public_read"
})
public class SampleACLs {

    @JsonProperty("owner")
    private java.lang.String owner;
    @JsonProperty("admin")
    private List<String> admin;
    @JsonProperty("write")
    private List<String> write;
    @JsonProperty("read")
    private List<String> read;
    @JsonProperty("public_read")
    private Long publicRead;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("owner")
    public java.lang.String getOwner() {
        return owner;
    }

    @JsonProperty("owner")
    public void setOwner(java.lang.String owner) {
        this.owner = owner;
    }

    public SampleACLs withOwner(java.lang.String owner) {
        this.owner = owner;
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

    public SampleACLs withAdmin(List<String> admin) {
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

    public SampleACLs withWrite(List<String> write) {
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

    public SampleACLs withRead(List<String> read) {
        this.read = read;
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

    public SampleACLs withPublicRead(Long publicRead) {
        this.publicRead = publicRead;
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
        return ((((((((((((("SampleACLs"+" [owner=")+ owner)+", admin=")+ admin)+", write=")+ write)+", read=")+ read)+", publicRead=")+ publicRead)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
