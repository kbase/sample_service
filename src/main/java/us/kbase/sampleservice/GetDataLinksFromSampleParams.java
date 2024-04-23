
package us.kbase.sampleservice;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: GetDataLinksFromSampleParams</p>
 * <pre>
 * get_data_links_from_sample parameters.
 *         id - the sample ID.
 *         version - the sample version.
 *         effective_time - the effective time at which the query should be run - the default is
 *             the current time. Providing a time allows for reproducibility of previous results.
 *         as_admin - run the method as a service administrator. The user must have read
 *             administration permissions.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "id",
    "version",
    "effective_time",
    "as_admin"
})
public class GetDataLinksFromSampleParams {

    @JsonProperty("id")
    private String id;
    @JsonProperty("version")
    private Long version;
    @JsonProperty("effective_time")
    private Long effectiveTime;
    @JsonProperty("as_admin")
    private Long asAdmin;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("id")
    public String getId() {
        return id;
    }

    @JsonProperty("id")
    public void setId(String id) {
        this.id = id;
    }

    public GetDataLinksFromSampleParams withId(String id) {
        this.id = id;
        return this;
    }

    @JsonProperty("version")
    public Long getVersion() {
        return version;
    }

    @JsonProperty("version")
    public void setVersion(Long version) {
        this.version = version;
    }

    public GetDataLinksFromSampleParams withVersion(Long version) {
        this.version = version;
        return this;
    }

    @JsonProperty("effective_time")
    public Long getEffectiveTime() {
        return effectiveTime;
    }

    @JsonProperty("effective_time")
    public void setEffectiveTime(Long effectiveTime) {
        this.effectiveTime = effectiveTime;
    }

    public GetDataLinksFromSampleParams withEffectiveTime(Long effectiveTime) {
        this.effectiveTime = effectiveTime;
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

    public GetDataLinksFromSampleParams withAsAdmin(Long asAdmin) {
        this.asAdmin = asAdmin;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((("GetDataLinksFromSampleParams"+" [id=")+ id)+", version=")+ version)+", effectiveTime=")+ effectiveTime)+", asAdmin=")+ asAdmin)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
